from urlparse import urlparse, parse_qsl

from django.test import TestCase,  RequestFactory
from django.shortcuts import reverse, Http404
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

from homes_user.views import UserDashboardPageView, UserSubscribeView, UserFavouriteView
from homes.factories.user_factory import UserFactory
from homes.factories.group_factory import GroupFactory
from homes_for_sale.factories.sale_favourite_factory import SaleFavouriteFactory
from homes_to_let.factories.letting_favourite_factory import LettingFavouriteFactory
from homes_for_sale.factories.sale_factory import SaleFactory
from homes.factories.alert_factory import AlertFactory
from homes_to_let.models import LettingFavourite
from homes_for_sale.models import SaleFavourite
from homes.models import Alert


class BaseTestCase(TestCase):
    """Base test case with common functions"""
    def setUp(self):
        """
        Create a request factory
        """
        self.factory = RequestFactory()

    def initialize(self, view, request, *args, **kwargs):
        """
        Sets up view for testing
        """
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def parse_url(self, response):
        url = urlparse(response.url)
        query = dict(parse_qsl(url.query))
        return url, query

    def enable_middleware(self, request):
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        return request


class UserFavouriteViewTestCase(BaseTestCase):
    def test_user_anonymous_redirected(self):
        """
        Test that on hitting the favourite function when anonymous get redirect to login
        """
        sale = SaleFactory()

        request = self.factory.get(reverse('user:favourite', kwargs={'type': 'sale', 'slug': sale.slug}))
        request.user = AnonymousUser()

        response = UserFavouriteView.as_view()(request)

        # Check that status code is 302 and redirect url is as expected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/user/favourite/sale/{}/'.format(sale.slug))

    def test_user_logged_in_not_in_group(self):
        """
        Test that on hitting the favourite function when logged in, but not in group causes redirect
        """
        sale = SaleFactory()

        request = self.factory.get(reverse('user:favourite', kwargs={'type': 'sale', 'slug': sale.slug}))
        request.user = UserFactory()

        response = UserFavouriteView.as_view()(request)

        # Check that status code is 302 and redirect url is as expected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/user/favourite/sale/{}/'.format(sale.slug))

    def test_user_delete_favourite(self):
        """
        Test that on hitting the delete favourite function when logged in, and in group causes favourite
        to be deleted
        """
        sale = SaleFactory()
        user = UserFactory.create(groups=[GroupFactory(name='general')])

        SaleFavouriteFactory(property=sale, user=user)

        request = self.factory.get(reverse('user:favourite', kwargs={'type': 'sale', 'slug': sale.slug}))
        request.user = user

        request = self.enable_middleware(request)

        response = UserFavouriteView.as_view()(request, type='sale', slug=sale.slug)

        favourites = SaleFavourite.objects.filter(user=user, property__slug=sale.slug)

        # Check that status code is 302 and redirect url is as expected and that the existing favourite was deleted
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/dashboard/')
        self.assertTrue(len(favourites) == 0)

    def test_user_delete_favourite_property_missing(self):
        """
        Test that on hitting the delete favourite function when logged in, and in group causes 404 if property
        doesnt exist to delete user favourite from
        """
        user = UserFactory.create(groups=[GroupFactory(name='general')])

        request = self.factory.get(reverse('user:favourite', kwargs={'type': 'sale', 'slug': 'test'}))
        request.user = user

        request = self.enable_middleware(request)

        with self.assertRaises(Http404):
            UserFavouriteView.as_view()(request, type='sale', slug='test')


class UserDashboardPageViewTestCase(BaseTestCase):
    def test_user_anonymous_redirected(self):
        """
        Test that on hitting the user dashboard when anonymous get redirect to login
        """
        request = self.factory.get(reverse('user:dashboard'))
        request.user = AnonymousUser()

        response = UserDashboardPageView.as_view()(request)

        # Check that status code is 302 and redirect url is as expected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,'/accounts/login/?next=/user/dashboard/')

    def test_user_logged_in_not_in_group(self):
        """
        Test that on hitting the user dashboard when logged in, but not in group causes redirect
        """
        request = self.factory.get(reverse('user:dashboard'))
        request.user = UserFactory()

        response = UserDashboardPageView.as_view()(request)

        # Check that status code is 302 and redirect url is as expected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,'/accounts/login/?next=/user/dashboard/')

    def test_user_logged_in_and_in_group(self):
        """
        Test when user logged in and in general group that the dashboard loads
        """
        request = self.factory.get(reverse('user:dashboard'))
        request.user = UserFactory.create(groups=[GroupFactory(name='general')])

        response = UserDashboardPageView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn('homes-user/dashboard.html', response.template_name)

    def test_get_context(self):
        """
        Test get_context for a logged in user in required group
        """
        request = self.factory.get(reverse('user:dashboard'))
        request.user = UserFactory.create(groups=[GroupFactory(name='general')])

        response = UserDashboardPageView.as_view()(request)

        # Check context has favourites, favourites.sale and favourites.letting and that
        # it also has alerts
        self.assertIn('favourites',response.context_data)
        self.assertIn('sale', response.context_data['favourites'])
        self.assertIn('letting', response.context_data['favourites'])
        self.assertIn('alerts', response.context_data)

    def test_get_context_user_has_favourites(self):
        """
        Test that when user has favourites in sale and letting that they are returned
        """
        user = UserFactory.create(groups=[GroupFactory(name='general')])

        SaleFavouriteFactory(user=user)
        LettingFavouriteFactory(user=user)

        request = self.factory.get(reverse('user:dashboard'))
        request.user = user

        response = UserDashboardPageView.as_view()(request)

        self.assertTrue(len(response.context_data['favourites']['sale']) == 1)
        self.assertTrue(len(response.context_data['favourites']['letting']) == 1)
        self.assertIsInstance(response.context_data['favourites']['sale'][0], SaleFavourite)
        self.assertIsInstance(response.context_data['favourites']['letting'][0], LettingFavourite)

    def test_get_context_user_has_alerts(self):
        """
        Test that when user has alerts they are returned
        """
        user = UserFactory.create(groups=[GroupFactory(name='general')])

        AlertFactory(user=user)

        request = self.factory.get(reverse('user:dashboard'))
        request.user = user

        response = UserDashboardPageView.as_view()(request)

        self.assertTrue(len(response.context_data['alerts']) == 1)
        self.assertIsInstance(response.context_data['alerts'][0], Alert)


class SubscribeViewTestCase(BaseTestCase):
    def test_user_anonymous_redirected(self):
        """
        Test that on hitting the subscribe function when anonymous get redirect to login
        """
        request = self.factory.get(reverse('user:subscribe'))
        request.user = AnonymousUser()

        response = UserSubscribeView.as_view()(request)

        # Check that status code is 302 and redirect url is as expected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/user/subscribe/')

    def test_user_logged_in_not_in_group(self):
        """
        Test that on hitting the subscribe function when logged in, but not in group causes redirect
        """
        request = self.factory.get(reverse('user:subscribe'))
        request.user = UserFactory()

        response = UserSubscribeView.as_view()(request)

        # Check that status code is 302 and redirect url is as expected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,'/accounts/login/?next=/user/subscribe/')

    def test_get_will_subscribed(self):
        """
        Test that subscribe if not subscribed user is subscribed and redirected back to referer
        """
        request = self.factory.get(reverse('user:subscribe') + "?test1=test&test2=test", HTTP_REFERER='/test/')
        request.user = UserFactory.create(groups=[GroupFactory(name='general')])

        request = super(SubscribeViewTestCase, self).enable_middleware(request)

        response = UserSubscribeView.as_view()(request)

        alerts = Alert.objects.filter(user=request.user)

        # Check status code is 302 and that the url being redirected back to is /test/ and that the alert is added
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/test/')
        self.assertTrue(len(alerts) == 1)

    def test_get_will_unsubscribe(self):
        """
        Test that subscribe if not subscribed user is subscribed and redirected back to referer
        """
        user = UserFactory.create(groups=[GroupFactory(name='general')])
        alert = AlertFactory(user=user, criteria={'test1':'test','test2':'test'})

        request = self.factory.get(reverse('user:subscribe') + "?test1=test&test2=test", HTTP_REFERER='/test/')
        request.user = user

        request = super(SubscribeViewTestCase, self).enable_middleware(request)

        response = UserSubscribeView.as_view()(request)

        alerts = Alert.objects.filter(user=user)

        # Check status code is 302 and that the url being redirected
        # back to is /test/ and that the alert is removed
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/test/')
        self.assertTrue(len(alerts) == 0)
