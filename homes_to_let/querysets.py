from datetime import datetime

from django.contrib.gis.db import models

from homes.behaviours import Publishable

import pytz


class LettingQuerySet(models.query.QuerySet):
    def published(self):
        return self.filter(status=Publishable.STATUS_CHOICE_ACTIVE)

    def unpublished(self):
        return self.filter(status=Publishable.STATUS_CHOICE_INACTIVE)

    def unexpired(self):
        return self.filter(expires_at__isnull=True) | self.filter(expires_at__gt=datetime.utcnow().replace(tzinfo=pytz.utc))

    def expired(self):
        return self.filter(expires_at__lte=datetime.utcnow().replace(tzinfo=pytz.utc))

    def available(self):
        return self.filter(available_at__gt=datetime.utcnow().replace(tzinfo=pytz.utc))

    def unavailable(self):
        return self.filter(available_at__lte=datetime.utcnow().replace(tzinfo=pytz.utc))

    def let_agreed(self):
        return self.filter(let_agreed=True)

    def let_not_agreed(self):
        return self.filter(let_agreed=False)

    def furnished(self):
        return self.filter(furnished=True)

    def unfurnished(self):
        return self.filter(furnished=False)

    def type_of_let(self, type):
        return self.filter(type_of_let=type)

    def house_share(self):
        return self.filter(house_share=True)