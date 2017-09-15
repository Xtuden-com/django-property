from datetime import datetime, timedelta

from django.test import TestCase

from homes_for_sale.factories.sale_factory import SaleFactory
from homes.factories.property_tenure_factory import PropertyTenureFactory
from homes_for_sale.models import Sale

import pytz

class SaleQuerySetTestCase(TestCase):

    def test_published_queryset(self):
        sales = [
            SaleFactory(status=Sale.STATUS_CHOICE_ACTIVE),
            SaleFactory(status=Sale.STATUS_CHOICE_INACTIVE)
        ]
        results = Sale.filtered.published()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, sales[0].title)

    def test_unpublished_queryset(self):
        sales = [
            SaleFactory(status=Sale.STATUS_CHOICE_ACTIVE),
            SaleFactory(status=Sale.STATUS_CHOICE_INACTIVE)
        ]
        results = Sale.filtered.unpublished()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, sales[1].title)

    def test_unexpired_queryset(self):
        sales = [
            SaleFactory(expires_at=datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=30)),
            SaleFactory(expires_at=datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=-30))
        ]
        results = Sale.filtered.unexpired()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, sales[0].title)

    def test_expired_queryset(self):
        sales = [
            SaleFactory(expires_at=datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=30)),
            SaleFactory(expires_at=datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=-30))
        ]
        results = Sale.filtered.expired()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, sales[1].title)

    def test_new_home_queryset(self):
        sales = [
            SaleFactory(new_home=True),
            SaleFactory(new_home=False)
        ]
        results = Sale.filtered.new_home()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, sales[0].title)

    def test_shared_ownership_queryset(self):
        sales = [
            SaleFactory(shared_ownership=True),
            SaleFactory(shared_ownership=False)
        ]
        results = Sale.filtered.shared_ownership()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, sales[0].title)

    def test_auction_queryset(self):
        sales = [
            SaleFactory(auction=True),
            SaleFactory(auction=False)
        ]
        results = Sale.filtered.auction()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, sales[0].title)

    def test_property_tenure_queryset(self):
        sales = [
            SaleFactory(property_tenure=PropertyTenureFactory(slug='test',name='Test')),
            SaleFactory()
        ]
        results = Sale.filtered.tenure('test')
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, sales[0].title)