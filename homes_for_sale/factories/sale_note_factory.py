from faker import Factory

from homes_for_sale.models import SaleNote
from homes_for_sale.factories.sale_factory import SaleFactory

import factory

fake = Factory.create('en_GB')


class SaleNoteFactory(factory.DjangoModelFactory):

    class Meta:
        model = SaleNote

    property = factory.SubFactory(SaleFactory)
    text = fake.text(100)
