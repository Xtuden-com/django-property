from faker import Factory

from homes_for_sale.models import SaleContact
from homes_for_sale.factories.sale_factory import SaleFactory

import factory, random

fake = Factory.create('en_GB')


class SaleContactFactory(factory.DjangoModelFactory):

    class Meta:
        model = SaleContact

    property = factory.SubFactory(SaleFactory)
    more_details = random.choice([True, False])
    view_property = random.choice([True, False])
    title = fake.prefix()
    forename = fake.first_name()
    surname = fake.last_name()
    message = fake.text(100)
    telephone = fake.phone_number()
    email = fake.safe_email()
    country = fake.country()
    postcode = fake.postcode()
