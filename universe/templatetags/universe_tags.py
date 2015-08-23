
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def afford_build(context, item, text):
    ship = context['ship']
    cost = ship.COST_BUILD[item]
    if ship.metal >= cost:
        url = reverse('build', args=(item,))
        link = '<a href="' + url + '">' + text + '</a>'
    else:
        link = '<span class="costly">' + text + '</span>'
    return link + ' ' + str(cost)


@register.simple_tag(takes_context=True)
def afford_research(context, item, text):
    ship = context['ship']
    cost = ship.research_cost(item)
    if ship.research >= cost:
        url = reverse('research', args=(item,))
        link = '<a href="' + url + '">' + text + '</a>'
    else:
        link = '<span class="costly">' + text + '</span>'
    return link + ' ' + str(cost)

