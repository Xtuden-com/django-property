from django.utils.text import slugify

from faker import Factory

from homes.models import MediaType

import factory

fake = Factory.create('en_GB')


class MediaTypeFactory(factory.DjangoModelFactory):

    class Meta:
        model = MediaType

    name = factory.Sequence(lambda n: fake.text(10) + '%s' % n)
    slug = factory.LazyAttribute(lambda a: slugify(a.name))
    status = MediaType.STATUS_CHOICE_ACTIVE