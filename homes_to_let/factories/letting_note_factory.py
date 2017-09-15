from faker import Factory

from homes_to_let.models import LettingNote
from homes_to_let.factories.letting_factory import LettingFactory

import factory

fake = Factory.create('en_GB')


class LettingNoteFactory(factory.DjangoModelFactory):

    class Meta:
        model = LettingNote

    property = factory.SubFactory(LettingFactory)
    text = fake.text(100)
