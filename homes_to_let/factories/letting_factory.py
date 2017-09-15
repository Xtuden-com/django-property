from datetime import datetime, timedelta

from django.utils.text import slugify

from faker import Factory

from homes_to_let.models import Letting
from homes.factories.property_type_factory import PropertyTypeFactory
from homes.factories.point_factory import FuzzyPoint
from homes.factories.branch_factory import BranchFactory

import factory, random, pytz

fake = Factory.create('en_GB')


class LettingFactory(factory.DjangoModelFactory):

    class Meta:
        model = Letting

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

    # Letting Fields
    rental = random.uniform(500.00,5000.00)
    period = random.randrange(1, len(Letting.RENTAL_PERIOD_CHOICES))
    type_of_let = random.randrange(1, len(Letting.TYPE_OF_LET_CHOICES))
    furnished = random.choice([True, False])
    house_share = random.choice([True, False])
    let_agreed = random.choice([True, False])
    available_at = datetime.utcnow().replace(tzinfo=pytz.utc) + timedelta(days=random.randrange(1,30))
