from faker import Factory

from homes_to_let.models import LettingMedia
from homes_to_let.factories.letting_factory import LettingFactory
from homes.factories.media_type_factory import MediaTypeFactory

import factory, random

fake = Factory.create('en_GB')


class LettingMediaFactory(factory.DjangoModelFactory):

    class Meta:
        model = LettingMedia

    property = factory.SubFactory(LettingFactory)
    media_type = factory.SubFactory(MediaTypeFactory)
    description = fake.text(10)
    attachment = fake.file_path(depth=1, category=None, extension='pdf')
    status = 1