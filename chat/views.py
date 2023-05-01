# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from chat.serializers import ChatRoomSerializer, ChatMessageSerializer
from chat.models import ChatRoom, ChatMessage

class ChatRoomView(APIView):
	def get(self, request, userId):
		chatRooms = ChatRoom.objects.filter(member=userId)
		serializer = ChatRoomSerializer(
			chatRooms, many=True, context={"request": request}
		)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = ChatRoomSerializer(
			data=request.data, context={"request": request}
		)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class MessagesView(APIView):
    def get(self, request, roomId):
        chat_room = ChatRoom.objects.get(roomId=roomId)
        chat_messages = ChatMessage.objects.filter(chat=chat_room).order_by('-timestamp')
        data = ChatMessageSerializer(chat_messages, many=True).data
        return Response({"chatRoomName": chat_room.name, "results": data})