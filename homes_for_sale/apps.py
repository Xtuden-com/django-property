# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class HomesForSaleConfig(AppConfig):
    name = 'homes_for_sale'
    verbose_name = 'Homes For Sale'

    def ready(self):
        import signals
