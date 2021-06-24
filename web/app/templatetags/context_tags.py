from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def message_kind(context, kind):
    messages = None
    if kind:
        if kind == 'bok':
            messages = context.get('BOK_MESSAGES', None)
        else:
            messages = context.get('PLANET_MESSAGES', None)

    return messages

@register.simple_tag()
def url_name(kind):
    name = None
    if kind:
        if kind == 'bok':
            name = 'bok-board'
        else:
            name = 'planet-board'
    return name
