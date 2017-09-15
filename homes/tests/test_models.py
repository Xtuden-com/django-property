from django.test import TestCase

from homes.factories.search_price_factory import SearchPriceFactory
from homes.factories.property_type_factory import PropertyTypeFactory
from homes.factories.alert_factory import AlertFactory
from homes.factories.media_type_factory import MediaTypeFactory
from homes.factories.property_tenure_factory import PropertyTenureFactory
from homes.factories.branch_factory import BranchFactory


class SearchPriceTestCase(TestCase):

    def test_string_representation(self):
        search_price = SearchPriceFactory()
        self.assertEquals(str(search_price), search_price.label)


class BranchTestCase(TestCase):

    def test_string_representation(self):
        branch = BranchFactory()
        self.assertEquals(str(branch), branch.name)


class PropertyTypeModelTestCase(TestCase):

    def test_string_representation(self):
        property_type = PropertyTypeFactory()
        self.assertEquals(str(property_type), property_type.name)


class MediaTypeModelTestCase(TestCase):

    def test_string_representation(self):
        media_type = MediaTypeFactory()
        self.assertEquals(str(media_type), media_type.name)


class PropertyTenureModelTestCase(TestCase):

    def test_string_representation(self):
        property_tenure = PropertyTenureFactory()
        self.assertEquals(str(property_tenure), property_tenure.name)


class AlertModelTestCase(TestCase):

    def test_string_representation(self):
        alert = AlertFactory()
        self.assertEquals(str(alert), alert.user.username)
