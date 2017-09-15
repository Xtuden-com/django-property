from datetime import datetime, timedelta

from django.test import TestCase

from homes_to_let.factories.letting_factory import LettingFactory
from homes_to_let.models import Letting

import pytz

class SaleQuerySetTestCase(TestCase):

    def test_published_queryset(self):
        lettings = [
            LettingFactory(status=Letting.STATUS_CHOICE_ACTIVE),
            LettingFactory(status=Letting.STATUS_CHOICE_INACTIVE)
        ]
        results = Letting.filtered.published()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, lettings[0].title)

    def test_unpublished_queryset(self):
        lettings = [
            LettingFactory(status=Letting.STATUS_CHOICE_ACTIVE),
            LettingFactory(status=Letting.STATUS_CHOICE_INACTIVE)
        ]
        results = Letting.filtered.unpublished()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, lettings[1].title)

    def test_unexpired_queryset(self):
        lettings = [
            LettingFactory(expires_at=datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=30)),
            LettingFactory(expires_at=datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=-30))
        ]
        results = Letting.filtered.unexpired()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, lettings[0].title)

    def test_expired_queryset(self):
        lettings = [
            LettingFactory(expires_at=datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=30)),
            LettingFactory(expires_at=datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=-30))
        ]
        results = Letting.filtered.expired()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, lettings[1].title)

    def test_let_agreed_queryset(self):
        lettings = [
            LettingFactory(let_agreed=True),
            LettingFactory(let_agreed=False)
        ]
        results = Letting.filtered.let_agreed()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, lettings[0].title)

    def test_let_not_agreed_queryset(self):
        lettings = [
            LettingFactory(let_agreed=True),
            LettingFactory(let_agreed=False)
        ]
        results = Letting.filtered.let_not_agreed()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, lettings[1].title)

    def test_furnished_queryset(self):
        lettings = [
            LettingFactory(furnished=True),
            LettingFactory(furnished=False)
        ]
        results = Letting.filtered.furnished()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, lettings[0].title)

    def test_unfurnished_queryset(self):
        lettings = [
            LettingFactory(furnished=True),
            LettingFactory(furnished=False)
        ]
        results = Letting.filtered.unfurnished()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, lettings[1].title)

    def test_type_of_let_queryset(self):
        lettings = [
            LettingFactory(type_of_let=Letting.TYPE_OF_LET_LONG_TERM),
            LettingFactory(type_of_let=Letting.TYPE_OF_LET_SHORT_TERM)
        ]
        results = Letting.filtered.type_of_let(Letting.TYPE_OF_LET_LONG_TERM)
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, lettings[0].title)

    def test_house_share_queryset(self):
        lettings = [
            LettingFactory(house_share=True),
            LettingFactory(house_share=False)
        ]
        results = Letting.filtered.house_share()
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].title, lettings[0].title)