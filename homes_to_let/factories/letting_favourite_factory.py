from faker import Factory

from homes_to_let.models import LettingFavourite
from homes_to_let.factories.letting_factory import LettingFactory
from homes.factories.user_factory import UserFactory

import factory

fake = Factory.create('en_GB')


class LettingFavouriteFactory(factory.DjangoModelFactory):

    class Meta:
        model = LettingFavourite

    property = factory.SubFactory(LettingFactory)
    user = factory.SubFactory(UserFactory)
