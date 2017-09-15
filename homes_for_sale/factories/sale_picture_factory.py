from faker import Factory

from homes_for_sale.models import SalePicture
from homes_for_sale.factories.sale_factory import SaleFactory

import factory

fake = Factory.create('en_GB')


class SalePictureFactory(factory.DjangoModelFactory):

    class Meta:
        model = SalePicture

    property = factory.SubFactory(SaleFactory)
    caption = fake.text(10)
    attachment = fake.file_path(depth=1, category=None, extension='jpg')
    display_order = 1
    status = 1