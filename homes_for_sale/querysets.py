from datetime import datetime

from django.contrib.gis.db import models

from homes.behaviours import Publishable

import pytz


class SaleQuerySet(models.query.QuerySet):
    def published(self):
        return self.filter(status=Publishable.STATUS_CHOICE_ACTIVE)

    def unpublished(self):
        return self.filter(status=Publishable.STATUS_CHOICE_INACTIVE)

    def unexpired(self):
        return self.filter(expires_at__isnull=True) | self.filter(expires_at__gt=datetime.utcnow().replace(tzinfo=pytz.utc))

    def expired(self):
        return self.filter(expires_at__lte=datetime.utcnow().replace(tzinfo=pytz.utc))

    def new_home(self):
        return self.filter(new_home=True)

    def shared_ownership(self):
        return self.filter(shared_ownership=True)

    def auction(self):
        return self.filter(auction=True)

    def tenure(self, slug):
        return self.filter(property_tenure__slug=slug)