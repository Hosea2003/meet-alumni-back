from rest_framework import serializers

from message.models import Message
from user.models import User


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class UserMessageSerializer(serializers.ModelSerializer):
    profile_picture=serializers.SerializerMethodField()
    class Meta:
        model = User
        fields=["id", "first_name","last_name", "profile_picture"]

    def get_profile_picture(self, user):
        pf = user.profile_picture
        if pf:
            return pf.url
        return "/media/pf/user.png"

class MessageUserSerializer(serializers.Serializer):
    friend = UserMessageSerializer()
    content=serializers.CharField()
    dateSend=serializers.DateTimeField()
    lastSenderMe = serializers.BooleanField()