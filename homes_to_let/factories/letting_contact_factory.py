from faker import Factory

from homes_to_let.models import LettingContact
from homes_to_let.factories.letting_factory import LettingFactory

import factory, random

fake = Factory.create('en_GB')


class LettingContactFactory(factory.DjangoModelFactory):

    class Meta:
        model = LettingContact

    property = factory.SubFactory(LettingFactory)
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
