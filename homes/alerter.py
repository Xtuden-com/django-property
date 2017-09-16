import logging

from django.contrib.gis.geos import GEOSGeometry, GEOSException
from django.contrib.gis.measure import D
from django.conf import settings

from homes.models import Alert
from homes_for_sale.models import Sale
from homes_to_let.models import Letting
from homes.emailer import Emailer


class Alerter(object):
    logger = logging.getLogger('management')

    def __init__(self):
        pass

    def __get_point(self, criteria):
        try:
            return GEOSGeometry('POINT(%s %s)' % (criteria.get('longitude'), criteria.get('latitude')), srid=4326)
        except GEOSException as ex:
            self.logger.error('GEOS Exception for longitude / latitude')
            self.logger.error(ex)
        return False

    def __get_lettings_search(self, criteria):
        lettings = Letting.filtered.published().unexpired()
        lettings = lettings.filter(
            price__range=(
                criteria.get('min_price',10000),
                criteria.get('max_price',1000000)
            )
        )
        lettings = lettings.filter(bedrooms__gte=criteria.get('min_bedrooms',0))
        lettings = lettings.filter(property_type__slug=criteria.get('property_type','house'))
        lettings = lettings.filter(location__distance_lte=(self.__get_point(criteria),D(mi=criteria.get('distance',10))))
        lettings = lettings.order_by('-created_at')[:5]
        return lettings

    def __get_sales_search(self, criteria):
        sales = Sale.filtered.published().unexpired()
        sales = sales.filter(
            price__range=(
                criteria.get('min_price',10000),
                criteria.get('max_price',1000000)
            )
        )
        sales = sales.filter(bedrooms__gte=criteria.get('min_bedrooms',0))
        sales = sales.filter(property_type__slug=criteria.get('property_type','house'))
        sales = sales.filter(location__distance_lte=(self.__get_point(criteria),D(mi=criteria.get('distance',10))))
        sales = sales.order_by('-created_at')[:5]
        return sales

    def __filter_alerts_to_send(self):
        alerts_to_send = {}
        for alert in Alert.objects.all():
            if not alert.key in alerts_to_send:
                alerts_to_send[alert.key] = {'criteria': alert.criteria, 'recipients': []}
            alerts_to_send[alert.key]['recipients'].append(alert.user.email)
        return alerts_to_send

    def __send(self, recipients, properties):
        for recipient in recipients:
            #self, subject, recipient, from_email, reply_to, data, filename):
            mailer = Emailer('Property Alerts', [recipient], settings.DO_NOT_REPLY_EMAIL, ['me@example.com'], {'properties':properties}, 'emails/alerts.txt')
            mailer.send()

    def process(self):
        alerts_to_send = self.__filter_alerts_to_send()
        for key, config in alerts_to_send.iteritems():
            if config['criteria']['search_type'] == 'sales':
                properties = self.__get_sales_search(config['criteria'])
            else:
                properties = self.__get_lettings_search(config['criteria'])
            if len(properties) > 0:
                self.__send(config['recipients'], properties)
            else:
                self.logger.info('No properties to send for alert key {}'.format(key))