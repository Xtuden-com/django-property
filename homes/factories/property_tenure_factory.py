from django.utils.text import slugify

from faker import Factory

from homes.models import PropertyTenure

import factory

fake = Factory.create('en_GB')


class PropertyTenureFactory(factory.DjangoModelFactory):

    class Meta:
        model = PropertyTenure

    name = factory.Sequence(lambda n: fake.text(10) + '%s' % n)
    slug = factory.LazyAttribute(lambda a: slugify(a.name))
    status = PropertyTenure.STATUS_CHOICE_ACTIVE