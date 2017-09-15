from django.utils.text import slugify

from faker import Factory

from homes.models import PropertyType

import factory

fake = Factory.create('en_GB')


class PropertyTypeFactory(factory.DjangoModelFactory):

    class Meta:
        model = PropertyType

    name = factory.Sequence(lambda n: fake.text(10) + '%s' % n)
    slug = factory.LazyAttribute(lambda a: slugify(a.name))
    status = PropertyType.STATUS_CHOICE_ACTIVE