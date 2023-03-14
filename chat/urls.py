from django.urls import path
from account.views import UserView
from .views import ChatRoomView, MessagesView

urlpatterns = [
	path('users', UserView.as_view(), name='userList'),
	path('chats/<str:roomId>/messages', MessagesView.as_view(), name='messageList'),
	path('users/<int:userId>/chats', ChatRoomView.as_view(), name='chatRoomList'),
]