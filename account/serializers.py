from .models import Account
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id','username', 'password','image']

    def create(self, validated_data):
        user = Account(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.image = validated_data.get('image')
        user.save()
        return user