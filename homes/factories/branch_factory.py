from django.utils.text import slugify

from faker import Factory

from homes.factories.point_factory import FuzzyPoint
from homes.models import Branch

import factory, random

fake = Factory.create('en_GB')


class BranchFactory(factory.DjangoModelFactory):

    class Meta:
        model = Branch

    name = factory.Sequence(lambda n: fake.text(10) + '%s' % n)
    slug = factory.LazyAttribute(lambda a: slugify(a.name))
    address_1 = fake.street_address()
    town_city = fake.city()
    county = fake.word()
    postcode = fake.postcode()
    location = FuzzyPoint()
    telephone = fake.phone_number()
    email = fake.safe_email()
    details = fake.text(100)
    opening_hours = fake.text(50)
    status = Branch.STATUS_CHOICE_ACTIVE

