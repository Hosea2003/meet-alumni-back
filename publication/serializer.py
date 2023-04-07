from rest_framework import serializers
from .models import Publication, PublicationLike, PublicationComment


class PublicationSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name")
    author_id = serializers.IntegerField(source="author.id")
    author_pdp = serializers.CharField(source="author.pdp_link")
    content = serializers.CharField(read_only=True)
    likesCount = serializers.IntegerField()
    commentsCount = serializers.IntegerField()
    image = serializers.ImageField(read_only=True)
    have_liked= serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = [
            "id",
            "author_name",
            "author_id",
            "author_pdp",
            "content",
            "datePub",
            "likesCount",
            "commentsCount",
            "image",
            "have_liked"
        ]

    def get_author_pdp(self, obj):
        pf = obj.author.profile_picture
        if pf:
            return pf.url
        return "/media/pf/user.png"

    def get_have_liked(self, post):
        connected_user=self.context.get("request").user
        return post.likes.filter(user=connected_user).count()>0

class WritePublicationSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = Publication
        fields=["id", "content", "image"]


class CommentSerializer(serializers.ModelSerializer):
    profile_image=serializers.CharField(source="user.pdp_link")
    user_name = serializers.CharField(source="user.name")
    comment = serializers.CharField()
    dateComment = serializers.DateTimeField()

    class Meta:
        model=PublicationComment
        fields=[
            "id",
            "profile_image",
            "user_name",
            "comment",
            "pub_id",
            "dateComment"
        ]
