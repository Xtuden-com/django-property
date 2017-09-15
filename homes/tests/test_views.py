from urlparse import urlparse, parse_qsl
from urllib import urlencode

from mock import patch, Mock

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import RequestFactory
from django.shortcuts import HttpResponseRedirect
from django.http import QueryDict

from homes.views import HomePageView, BaseSearchPageView
from homes.forms import SearchForm
from homes.factories.property_type_factory import PropertyTypeFactory
from homes.factories.search_price_factory import SearchPriceFactory
from homes.mocks.geocoder_mock import GeocoderMock, GeocoderErrorMock, GeocoderExceptionMock
from homes.models import SearchPrice


class BaseTestCase(TestCase):
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

    def get_data_sales(self):
        """
        Creates valid data for search for sale
        """
        return {
            'search_type': SearchForm.SEARCH_TYPE_SALE,
            'min_price': '40000',
            'max_price': '50000',
            'location':'Test, Test',
            'min_bedrooms': '5',
            'property_type': str(PropertyTypeFactory().slug)
        }

    def get_data_extra(self, initial):
        """
        Merge some extra values with initial values
        """
        extra = {
            'distance':'10',
            'latitude':'0',
            'longitude':'1'
        }
        return dict(initial.items() + extra.items())

    def get_data_lettings(self):
        """
        Creates valid data for search for let
        """
        return {
            'search_type': SearchForm.SEARCH_TYPE_LETTING,
            'min_price': '100',
            'max_price': '200',
            'location':'Test, Test',
            'min_bedrooms': '5',
            'property_type': str(PropertyTypeFactory().slug)
        }


class HomeViewTestCase(BaseTestCase):
    def test_view_response_via_url(self):
        """
        Test that when hitting the homepage you get a 200
        """
        request = self.factory.get(reverse('homepage'))

        response = HomePageView.as_view()(request)

        # Check that 200 is returned as status code
        self.assertEquals(response.status_code, 200)

    def test_get_context(self):
        """
        Test context data contains required items
        """
        request = self.factory.get(reverse('homepage'))

        response = HomePageView.as_view()(request)

        self.assertIn('form', response.context_data)
        self.assertIn('latest', response.context_data)
        self.assertIn('sale', response.context_data['latest'])
        self.assertIn('let', response.context_data['latest'])


class BaseSearchPageViewTestCase(BaseTestCase):

    def setUp(self):
        """
        Create a request factory and then create 4 prices for validation
        of SearchForm
        """
        super(BaseSearchPageViewTestCase, self).setUp()
        SearchPriceFactory(
            type=SearchPrice.SEARCH_PRICE_LETTING,
            label='100',
            price=100
        )
        SearchPriceFactory(
            type=SearchPrice.SEARCH_PRICE_LETTING,
            label='200',
            price=200
        )
        SearchPriceFactory(
            type=SearchPrice.SEARCH_PRICE_SALE,
            label='40000',
            price=40000
        )
        SearchPriceFactory(
            type=SearchPrice.SEARCH_PRICE_SALE,
            label='50000',
            price=50000
        )

    def test_view_get_initial(self):
        """
        Test to check that if the request is GET and if the request.GET contains
        the key 'search_type' then the get_initial value on view returns a Dictionary
        containing the required keys from GET to populate SearchForm
        """
        data = super(BaseSearchPageViewTestCase, self).get_data_sales()

        request = self.factory.get(reverse('sales:search') + '?' + urlencode(data))

        view = super(BaseSearchPageViewTestCase, self).initialize(BaseSearchPageView(), request)

        response = view.get_initial()

        # Iterate each value in response and check that it is as was in the query initially
        # passed
        for key, value in response.items():
            self.assertTrue(key in data and data[key] == str(value))

    @patch('geocoder.google')
    def test_view_form_valid_sales_method(self, google):
        """
        Creates a form with required data, calls the form_valid method
        on this form then checks that the form_valid method on class when passed
        this valid form attempts to redirect to an expected sales search URL
        """
        google.return_value = GeocoderMock()

        form_data = super(BaseSearchPageViewTestCase, self).get_data_sales()

        view = super(BaseSearchPageViewTestCase, self).initialize(BaseSearchPageView(), None)

        view.form_class = SearchForm

        form = SearchForm(form_data)

        form.is_valid()

        response = view.form_valid(form)

        (url, query) = super(BaseSearchPageViewTestCase, self).parse_url(response)

        form_data = super(BaseSearchPageViewTestCase, self).get_data_extra(form_data)

        for key, value in form_data.iteritems():
            self.assertTrue(key in query and query[key] == str(value))

        # Check we are dealing with a redirect and path as expected as sales/search
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(url.path, '/sales/search/')

    @patch('geocoder.google')
    def test_view_form_valid_lettings_method(self, google):
        """
        Creates a form with required data, calls the form_valid method
        on this form then checks that the form_valid method on class when passed
        this valid form attempts to redirect to an expected lettings search URL
        """
        google.return_value = GeocoderMock()

        form_data = super(BaseSearchPageViewTestCase, self).get_data_lettings()

        view = super(BaseSearchPageViewTestCase, self).initialize(BaseSearchPageView(), None)

        view.form_class = SearchForm

        form = SearchForm(form_data)

        form.is_valid()

        response = view.form_valid(form)

        (url, query) = super(BaseSearchPageViewTestCase, self).parse_url(response)

        form_data = super(BaseSearchPageViewTestCase, self).get_data_extra(form_data)

        for key, value in form_data.iteritems():
            self.assertTrue(key in query and query[key] == str(value))

        # Check we are dealing with a redirect and path as expected is lettings/search
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(url.path, '/lettings/search/')

    @patch('geocoder.google')
    def test_view_form_valid_error_method(self, google):
        """
        Creates form data and validates. When form_valid called
        geocoder causes error and should redirect to search error
        page
        """
        google.return_value = GeocoderErrorMock()

        form_data = super(BaseSearchPageViewTestCase, self).get_data_lettings()

        view = super(BaseSearchPageViewTestCase, self).initialize(BaseSearchPageView(), None)

        view.form_class = SearchForm

        form = SearchForm(form_data)

        form.is_valid()

        response = view.form_valid(form)

        # Check that a response redirect occurs and that the URL for redirect is search/error
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEquals(response.url, '/search/error')

    @patch('geocoder.google')
    def test_view_geocoder_success(self, google):
        """
        Fire a location against the Google geocoder and receive a response of latitude, longitude
        """
        google.return_value = GeocoderMock()

        view = super(BaseSearchPageViewTestCase, self).initialize(BaseSearchPageView(), None)

        response = view.geocode_location('Test, Test')

        # Check geocoder returns a list of [0,1]
        self.assertListEqual(response, [0,1])

    @patch('geocoder.google')
    def test_view_geocoder_error(self, google):
        """
        Fire a location against the Google geocoder and receive a false response
        """
        google.return_value = GeocoderErrorMock()

        view = super(BaseSearchPageViewTestCase, self).initialize(BaseSearchPageView(), None)

        response = view.geocode_location('Test, Test')

        # Check geocoder returns false
        self.assertFalse(response)

    @patch('geocoder.google')
    def test_view_geocoder_exception(self, google):
        """
        Fire a location against the Google geocoder and receive a false response
        """
        google.return_value = GeocoderExceptionMock()

        view = super(BaseSearchPageViewTestCase, self).initialize(BaseSearchPageView(), None)

        # Check that function raises exception
        self.assertRaises(Exception, view.geocode_location('Test, Test'))