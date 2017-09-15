from faker import Factory

from homes_for_sale.models import SaleFavourite
from homes_for_sale.factories.sale_factory import SaleFactory
from homes.factories.user_factory import UserFactory

import factory

fake = Factory.create('en_GB')


class SaleFavouriteFactory(factory.DjangoModelFactory):

    class Meta:
        model = SaleFavourite

    property = factory.SubFactory(SaleFactory)
    user = factory.SubFactory(UserFactory)
