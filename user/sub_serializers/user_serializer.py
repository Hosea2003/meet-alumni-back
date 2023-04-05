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

    isAdminCollege = serializers.BooleanField(read_only=True)

    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"

    def get_profile_picture(self, user):
        pf = user.profile_picture
        if pf:
            return pf.url
        return "/media/pf/user.png"


class ProfilePictureSerializer(serializers.ModelSerializer):

    user_id = serializers.ReadOnlyField(source="user.id")

    user = serializers.ReadOnlyField(source="user.first_name")

    image_url = serializers.ImageField(required=False)

    class Meta:
        model = ProfilePicture
        fields = ["id", "user_id", "user", "image_url"]