from django.urls import path
from . import views
urlpatterns = [
    path('dialogs/', views.DialogView, name='dialogs'),
    path('dialogs/<int:chat_id>', views.MessagesView.as_view(), name='messages'),
    path('dialogs/<int:chat_id>/messages', views.AllMessagesView.as_view(), name='list_messages'),
    path('search/', views.SearchResultsView.as_view(), name='search_user'),
    path('search/create/<int:user_id>', views.CreateDialogView.as_view(), name='create_dialog'),
]