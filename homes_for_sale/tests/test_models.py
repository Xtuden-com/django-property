from django.test import TestCase

from homes_for_sale.factories.sale_factory import SaleFactory
from homes_for_sale.factories.sale_feature_factory import SaleFeatureFactory
from homes_for_sale.factories.sale_picture_factory import SalePictureFactory
from homes_for_sale.factories.sale_media_factory import SaleMediaFactory
from homes_for_sale.factories.sale_contact_factory import SaleContactFactory
from homes_for_sale.factories.sale_note_factory import SaleNoteFactory
from homes_for_sale.factories.sale_favourite_factory import SaleFavouriteFactory


class SaleModelTestCase(TestCase):

    def test_string_representation(self):
        sale = SaleFactory()
        self.assertEquals(str(sale), sale.title)


class SaleFeatureModelTestCase(TestCase):

    def test_string_representation(self):
        feature = SaleFeatureFactory()
        self.assertEquals(str(feature), feature.text)


class SalePictureModelTestCase(TestCase):

    def test_string_representation(self):
        picture = SalePictureFactory()
        self.assertEquals(str(picture), picture.caption)


class SaleMediaModelTestCase(TestCase):

    def test_string_representation(self):
        media = SaleMediaFactory()
        self.assertEquals(str(media), media.description)


class SaleContactModelTestCase(TestCase):

    def test_string_representation(self):
        contact = SaleContactFactory()
        self.assertEquals(str(contact), "%s %s (%s)" % (contact.forename, contact.surname, contact.email))


class SaleNoteModelTestCase(TestCase):

    def test_string_representation(self):
        note = SaleNoteFactory()
        self.assertEquals(str(note), note.text)


class SaleFavouriteModelTestCase(TestCase):

    def test_string_representation(self):
        favourite = SaleFavouriteFactory()
        self.assertEquals(str(favourite), favourite.user.username)
