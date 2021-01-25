from django.shortcuts import render, redirect
from django.views import View
from django.forms import ModelForm
from .models import Chat, Message
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.db.models import Q,Count

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}


def home(request):
        return render(request, 'home.html')



class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0 and user_id != request.user.id :
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
            return redirect(reverse('messages', kwargs={'chat_id': chat.id}))
        elif user_id == request.user.id:
            return redirect(reverse('search_user'))
        else:
            chat = chats.first()
            return redirect(reverse('messages', kwargs={'chat_id': chat.id}))


class SearchResultsView(ListView):
    model = User
    template_name = 'search_user.html'

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        object_list = User.objects.filter(
            Q(username=query)
        )
        if object_list.count() == 1:
            return object_list
        else:
            object_list = 'A'
            return object_list


def DialogView(request):
    chats = Chat.objects.filter(members__in=[request.user.id])
    return render(request, 'chats.html', {'user_profile': request.user, 'chats': chats})


class MessagesView(View):

    def get(self, request, chat_id):
        if Chat.objects.filter(members__in=[request.user.id], id=chat_id):
            try:

                chat = Chat.objects.get(id=chat_id)

                last5 = len(Chat.objects.get(id=chat_id).message_set.all()) - 5
                if last5 > 5:
                    message = Chat.objects.get(id=chat_id).message_set.all()[last5::-1]
                else:
                    message = Chat.objects.get(id=chat_id).message_set.all()

            except Chat.DoesNotExist:
                chat = None

            return render(
                request,
                'chat.html',
                {
                    'user_profile': request.user,
                    'chat': chat,
                    'form': MessageForm(),
                    'message': message,
                }
            )

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('messages', kwargs={'chat_id': chat_id}))


class AllMessagesView(View):

    def get(self, request, chat_id):
        if Chat.objects.filter(members__in=[request.user.id], id=chat_id):
            try:

                chat = Chat.objects.get(id=chat_id)

            except Chat.DoesNotExist:
                chat = None

            return render(
                request,
                'list_messages.html',
                {
                    'user_profile': request.user,
                    'chat': chat,
                    'form': MessageForm(),
                }
            )
