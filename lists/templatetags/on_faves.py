from django import template

from lists.models import List

register = template.Library()


@register.simple_tag(takes_context=True)
def on_faves(context, room):
    user = context.request.user
    the_list = List.objects.get_or_none(user=user, name='My favorite rooms')
    if the_list is not None:
        return room in the_list.rooms.all()
    return False
