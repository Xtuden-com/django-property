from django import template

register = template.Library()

@register.inclusion_tag('templatetags/header.html')
def page_header(title):
    return {
        'title': title
    }
