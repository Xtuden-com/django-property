from faker import Factory

from homes_for_sale.models import SaleFeature
from homes_for_sale.factories.sale_factory import SaleFactory

import factory

fake = Factory.create('en_GB')


class SaleFeatureFactory(factory.DjangoModelFactory):

    class Meta:
        model = SaleFeature

    property = factory.SubFactory(SaleFactory)
    text = fake.text(10)
    display_order = 1