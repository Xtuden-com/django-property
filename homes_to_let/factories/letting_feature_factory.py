from faker import Factory

from homes_to_let.models import LettingFeature
from homes_to_let.factories.letting_factory import LettingFactory

import factory

fake = Factory.create('en_GB')


class LettingFeatureFactory(factory.DjangoModelFactory):

    class Meta:
        model = LettingFeature

    property = factory.SubFactory(LettingFactory)
    text = fake.text(10)
    display_order = 1