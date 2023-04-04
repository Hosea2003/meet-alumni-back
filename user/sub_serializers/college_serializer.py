from rest_framework import serializers

from user.sub_serializers.user_serializer import UserSerializer


class CollegeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    name = serializers.CharField(required=True)

    website = serializers.CharField()

    email = serializers.EmailField(required=True)

    address= serializers.CharField(required=True)

    admin = UserSerializer(required=False, write_only=True)

    contact = serializers.CharField(required=True)


class CollegeUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    # first_name = serializers.ReadOnlyField(source="user.first_name")
    #
    # last_name = serializers.ReadOnlyField(source="user.last_name")
    #
    # user_id = serializers.ReadOnlyField(source="user.id")

    user = UserSerializer(read_only=True)

    dateRequested=serializers.DateTimeField(read_only=True)