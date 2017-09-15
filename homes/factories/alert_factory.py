import hashlib
from faker import Factory

from homes.models import Alert
from homes.factories.user_factory import UserFactory

import factory

fake = Factory.create('en_GB')


class AlertFactory(factory.DjangoModelFactory):

    class Meta:
        model = Alert

    user = factory.SubFactory(UserFactory)
    key = factory.LazyAttribute(lambda a: hashlib.sha1(str(a.criteria)).hexdigest())
    criteria = {}
