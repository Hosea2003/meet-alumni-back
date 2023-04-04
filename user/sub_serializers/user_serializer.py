from rest_framework import serializers

from user.models import ProfilePicture, User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    email = serializers.EmailField(required=True)

    password = serializers.CharField(write_only=True)

    first_name = serializers.CharField(required=True)

    first_name = serializers.CharField(required=True)

    address = serializers.CharField(required=True)

    birthdate = serializers.DateField(required=True)

    gender = serializers.BooleanField(required=True)

    contact = serializers.CharField(required=True)

    isAdmin = serializers.BooleanField(read_only=True)

    profile_picture = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class ProfilePictureSerializer(serializers.ModelSerializer):

    user_id = serializers.ReadOnlyField(source="user.id")

    user = serializers.ReadOnlyField(source="user.first_name")

    image_url = serializers.ImageField(required=False)

    class Meta:
        model = ProfilePicture
        fields = ["id", "user_id", "user", "image_url"]