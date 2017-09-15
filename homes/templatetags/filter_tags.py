from urllib import urlencode
from django import template
from django.shortcuts import reverse
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='add_css')
def add_css(field, css):
    return field.as_widget(attrs={"class":css})

@register.filter(name='times')
def times(number, start=1):
    return range(start, number + 1)

@register.filter(name='format_criteria')
def format_criteria(criteria):
    params = dict(criteria)
    if params['min_bedrooms'] == '0':
        params['min_bedrooms'] = 'Studio'
    return "Bedrooms: {}, Location: {}, Type: {}, Price: {} - {}, Distance: {}".format(
        params['min_bedrooms'], params['location'], params['property_type'],
        params['min_price'], params['max_price'], params['distance']
    )

@register.filter(name='link_criteria')
def link_criteria(criteria):
    params = dict(criteria)
    url = reverse('sales:search') if params['search_type'] == 'sales' else reverse('lettings:search')
    return "{}?{}".format(url, urlencode(params))


@register.filter(name='delete_link_criteria')
def delete_link_criteria(criteria):
    return "{}?{}".format(reverse('user:subscribe'), urlencode(dict(criteria)))


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        has_group = group in user.groups.all()
    except:
        has_group = False
    return has_group
