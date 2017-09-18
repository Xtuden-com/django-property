from django import template

from homes.models import Block

register = template.Library()

@register.inclusion_tag('templatetags/header.html')
def page_header(title):
    return {
        'title': title
    }


@register.inclusion_tag('templatetags/block.html', takes_context=True)
def page_block(context, slug):
    block = Block.objects.filter(slug=slug).first()
    return {
        'block':block,
        'request': context['request']
    }