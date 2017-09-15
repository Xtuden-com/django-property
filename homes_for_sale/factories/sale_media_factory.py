from faker import Factory

from homes_for_sale.models import SaleMedia
from homes_for_sale.factories.sale_factory import SaleFactory
from homes.factories.media_type_factory import MediaTypeFactory

import factory, random

fake = Factory.create('en_GB')


class SaleMediaFactory(factory.DjangoModelFactory):

    class Meta:
        model = SaleMedia

    property = factory.SubFactory(SaleFactory)
    media_type = factory.SubFactory(MediaTypeFactory)
    description = fake.text(10)
    attachment = fake.file_path(depth=1, category=None, extension='pdf')
    status = 1