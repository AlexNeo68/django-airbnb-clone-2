from django.db.models import Q
from django.shortcuts import render

from conversations.models import Conversation
from users.models import User


# Create your views here.
def go_conversation(request, a_pk, b_pk):
    user1 = User.objects.get_or_none(pk=a_pk)
    user2 = User.objects.get_or_none(pk=b_pk)
    if user1 is not None and user2 is not None:
        conversation = Conversation.objects.get(Q(participants__in=[user1, user2]))
        print(conversation)
