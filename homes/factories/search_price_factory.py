from faker import Factory

from homes.models import SearchPrice

import factory, random

fake = Factory.create('en_GB')


class SearchPriceFactory(factory.DjangoModelFactory):

    class Meta:
        model = SearchPrice

    type = random.choice([1,2])
    label = factory.Sequence(lambda n: fake.text(10) + '%s' % n)
    price = random.uniform(100.00,1000000.00)
