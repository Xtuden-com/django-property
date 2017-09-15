from django.contrib.auth.models import Group

import factory


class GroupFactory(factory.DjangoModelFactory):

    class Meta:
        model = Group

    name = factory.Sequence(lambda n: "group%s" % n)
