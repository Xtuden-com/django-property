from faker import Factory

from homes_to_let.models import LettingPicture
from homes_to_let.factories.letting_factory import LettingFactory

import factory

fake = Factory.create('en_GB')


class LettingPictureFactory(factory.DjangoModelFactory):

    class Meta:
        model = LettingPicture

    property = factory.SubFactory(LettingFactory)
    caption = fake.text(10)
    attachment = fake.file_path(depth=1, category=None, extension='jpg')
    display_order = 1
    status = 1