from django.contrib.auth.models import User

from faker import Factory

import factory

fake = Factory.create('en_GB')


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Sequence(lambda n: fake.user_name() + '%s' % n)
    first_name = fake.name_male()
    email = fake.safe_email()
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)