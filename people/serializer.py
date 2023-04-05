from rest_framework import serializers

from people.models import Friend, FriendRequest
from user.models import User, CollegeUser

class PublicUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    mutual_friends = serializers.SerializerMethodField()

    profile_picture = serializers.SerializerMethodField()

    is_friend = serializers.SerializerMethodField()

    has_requested = serializers.SerializerMethodField()

    # what if I have requested to this user
    have_requested=serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "mutual_friends",
            "profile_picture",
            "is_friend",
            "has_requested",
            "have_requested"
        ]

    def get_name(self, obj: User):
        return obj.first_name + " " + obj.last_name

    def get_profile_picture(self, user):
        pf = user.profile_picture
        if pf:
            return pf.url
        return "/media/pf/user.png"

    def get_is_friend(self, obj):
        connected_user: User = self.context.get("request").user
        return connected_user.my_friends.filter(user2=obj).count() > 0

    def get_mutual_friends(self, user: User):
        connected_user: User = self.context.get("request").user
        user_friends = Friend.objects.filter(user1=user).values("user2")
        mutual_friends = Friend.objects.filter(user1=connected_user, user2__id__in=user_friends)
        return mutual_friends.count()

    def get_has_requested(self, user):
        connected_user = self.context.get("request").user
        return FriendRequest.objects.filter(sender=user, friend=connected_user).count() > 0

    def get_have_requested(self, user):
        connected_user = self.context.get("request").user
        print(connected_user)
        return FriendRequest.objects.filter(sender=connected_user, friend=user).count() > 0


class RequestSerializer(serializers.ModelSerializer):
    sender = PublicUserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        exclude = ["friend"]


class PublicCollegeUserSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer()

    class Meta:
        model = CollegeUser
        fields = ["id", "user", "isAlumni"]
