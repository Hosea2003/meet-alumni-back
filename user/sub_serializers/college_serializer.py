from rest_framework import serializers

from user.models import CollegeUser
from user.sub_serializers.user_serializer import UserSerializer


class CollegeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    name = serializers.CharField(required=True)

    website = serializers.CharField()

    email = serializers.EmailField(required=True)

    address = serializers.CharField(required=True)

    admin = UserSerializer(required=False, write_only=True)

    contact = serializers.CharField(required=True)


class CollegeUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    first_name = serializers.ReadOnlyField(source="user.first_name")

    last_name = serializers.ReadOnlyField(source="user.last_name")

    image = serializers.SerializerMethodField()

    dateRequested = serializers.DateTimeField(read_only=True)

    gender =serializers.BooleanField(source="user.gender")

    class Meta:
        model = CollegeUser
        fields = "__all__"

    def get_image(self, obj):
        user = obj.user
        pf= user.profile_picture
        if pf:
            return pf
        return "/media/pf/user.png"


class OtherCollegeSerializer(serializers.Serializer):
    college=CollegeSerializer()
    requestSent=serializers.BooleanField()