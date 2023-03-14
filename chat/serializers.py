from rest_framework import serializers
from chat.models import ChatRoom, ChatMessage
from account.serializers import AccountSerializer

class ChatRoomSerializer(serializers.ModelSerializer):
	member = AccountSerializer(many=True, read_only=True)
	members = serializers.ListField(write_only=True)

	def create(self, validatedData):
		memberObject = validatedData.pop('members')
		chatRoom = ChatRoom.objects.create(**validatedData)
		chatRoom.member.set(memberObject)
		return chatRoom

	class Meta:
		model = ChatRoom
		exclude = ['id']

class ChatMessageSerializer(serializers.ModelSerializer):
	userName = serializers.SerializerMethodField()
	userImage = serializers.ImageField(source='user.image')

	class Meta:
		model = ChatMessage
		exclude = ['id', 'chat']

	def get_userName(self, Obj):
		return Obj.user.username