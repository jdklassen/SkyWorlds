
from django import template
from django.core.urlresolvers import reverse
from django.templatetags.static import static

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
    return link + ' ' + str(cost) + r_icon('metal')


@register.simple_tag(takes_context=True)
def afford_research(context, item, text):
    ship = context['ship']
    cost = ship.research_cost(item)
    if ship.research >= cost:
        url = reverse('research', args=(item,))
        link = '<a href="' + url + '">' + text + '</a>'
    else:
        link = '<span class="costly">' + text + '</span>'
    return link + ' ' + str(cost) + r_icon('research')


_ICON_TYPES = {
    'population',
    'food',
    'metal',
    'farms',
    'miners',
    'research',
    'happiness',
    'restlessness',
}


@register.simple_tag
def r_icon(type):
    if type in _ICON_TYPES:
        path = static('universe/%s_icon.png' % type)
        return '<img alt="%s" src="%s">' % (type, path)
    return type

@register.simple_tag
def p_icon(planet):
    colour = 'barren'
    if planet.greenness > 60:
        colour = 'green'
    elif planet.greenness > 20:
        colour = 'desert'
    path = static('universe/planet_%s_icon.png' % colour)
    return '<img alt="%s planet" src="%s">' % (colour, path)

