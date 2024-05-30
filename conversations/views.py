from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, View

from conversations.models import Conversation, Message
from users.models import User


# Create your views here.
def go_conversation(request, a_pk, b_pk):
    user1 = User.objects.get_or_none(pk=a_pk)
    user2 = User.objects.get_or_none(pk=b_pk)
    if user1 is not None and user2 is not None:
        try:
            conversation = Conversation.objects.get(Q(participants=user1) & Q(participants=user2))
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create()
            conversation.participants.add(user1, user2)
        return redirect(conversation.get_absolute_url())


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        conversation = Conversation.objects.get(pk=pk)
        if not conversation:
            raise Http404
        return render(self.request, 'conversations/detail.html', {'conversation': conversation})

    def post(self, *args, **kwargs):
        pk = kwargs.get('pk')
        conversation = Conversation.objects.get(pk=pk)
        if not conversation:
            raise Http404
        message = self.request.POST.get('message', None)
        if message is not None and len(message) > 0:
            Message.objects.create(message=message, conversation=conversation, sender=self.request.user)

        return redirect(conversation.get_absolute_url())
