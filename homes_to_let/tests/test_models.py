from django.test import TestCase

from homes_to_let.factories.letting_factory import LettingFactory
from homes_to_let.factories.letting_feature_factory import LettingFeatureFactory
from homes_to_let.factories.letting_picture_factory import LettingPictureFactory
from homes_to_let.factories.letting_media_factory import LettingMediaFactory
from homes_to_let.factories.letting_contact_factory import LettingContactFactory
from homes_to_let.factories.letting_note_factory import LettingNoteFactory
from homes_to_let.factories.letting_favourite_factory import LettingFavouriteFactory

from homes_to_let.models import *


class LettingModelTestCase(TestCase):

    def test_string_representation(self):
        sale = LettingFactory()
        self.assertEquals(str(sale), sale.title)


class LettingFeatureModelTestCase(TestCase):

    def test_string_representation(self):
        feature = LettingFeatureFactory()
        self.assertEquals(str(feature), feature.text)


class LettingPictureModelTestCase(TestCase):

    def test_string_representation(self):
        picture = LettingPictureFactory()
        self.assertEquals(str(picture), picture.caption)


class LettingMediaModelTestCase(TestCase):

    def test_string_representation(self):
        media = LettingMediaFactory()
        self.assertEquals(str(media), media.description)


class LettingContactModelTestCase(TestCase):

    def test_string_representation(self):
        contact = LettingContactFactory()
        self.assertEquals(str(contact), "%s %s (%s)" % (contact.forename, contact.surname, contact.email))


class LettingNoteModelTestCase(TestCase):

    def test_string_representation(self):
        note = LettingNoteFactory()
        self.assertEquals(str(note), note.text)


class LettingFavouriteModelTestCase(TestCase):

    def test_string_representation(self):
        favourite = LettingFavouriteFactory()
        self.assertEquals(str(favourite), favourite.user.username)
