from django.utils.text import slugify

from faker import Factory

from homes_for_sale.models import Sale
from homes.factories.property_tenure_factory import PropertyTenureFactory
from homes.factories.property_type_factory import PropertyTypeFactory
from homes.factories.point_factory import FuzzyPoint
from homes.factories.branch_factory import BranchFactory

import factory, random

fake = Factory.create('en_GB')


class SaleFactory(factory.DjangoModelFactory):

    class Meta:
        model = Sale

    branch = factory.SubFactory(BranchFactory)
    property_type = factory.SubFactory(PropertyTypeFactory)
    title = fake.text(10)
    slug = factory.LazyAttribute(lambda a: slugify(a.title))
    address_1 = fake.street_address()
    town_city = fake.city()
    county = fake.word()
    postcode = fake.postcode()
    location = FuzzyPoint()
    display_address = fake.address()
    bedrooms = random.randrange(1,10)
    en_suites = random.randrange(1,10)
    receptions = random.randrange(1,10)
    details = fake.text(100)
    summary = fake.text(10)
    garden = random.choice([True, False])
    parking = random.choice([True, False])
    retirement = random.choice([True, False])
    status = 1

    # Sale Fields
    price = random.uniform(100000.00,1000000.00)
    qualifier = random.randrange(1, len(Sale.QUALIFIER_CHOICES))
    new_home = random.choice([True,False])
    shared_ownership = random.choice([True,False])
    auction = random.choice([True,False])
    property_tenure = factory.SubFactory(PropertyTenureFactory)