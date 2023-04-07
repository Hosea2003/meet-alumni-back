from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from api.utils import paginate
from rest_framework.permissions import IsAuthenticated

from people.models import Friend
from publication.models import Publication, PublicationLike, PublicationComment
from publication.serializer import WritePublicationSerializer, PublicationSerializer, CommentSerializer
from user.utils import getFromModel


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def publish(request:Request):
    user = request.user

    serializer = WritePublicationSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    publication = serializer.save(author=user)

    return Response(PublicationSerializer(publication).data, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def like_or_dislike_post(request:Request, pk):
    user = request.user
    post:Publication = getFromModel(Publication, pk)

#     check if already liked
    liked= post.likes.filter(user=user).first()

    if liked:
        liked.delete()

    else:
        PublicationLike.objects.create(
            pub=post,
            user=user
        )

    return Response(PublicationSerializer(post, context={"request":request}).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comment_post(request:Request, pk):
    user = request.user
    post: Publication = getFromModel(Publication, pk)

    comment = request.data.get("comment")

    if not comment:
        return Response("Provide a comment")

    comment = PublicationComment.objects.create(
        pub=post,
        user=user,
        comment=comment
    )

    return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_comments(request:Request, pk):
    post:Publication=getFromModel(Publication, pk)

    comments = PublicationComment.objects.filter(
        pub=post
    ).order_by("-dateComment")

    paginated=paginate(comments, request, CommentSerializer)

    return Response(paginated)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_posts(request:Request):
    user = request.user
    friends = Friend.objects.filter(user1=user)
    print(friends)
    posts=Publication.objects.filter(
        author_id__in=[user]+[friend.user2 for friend in friends]
    ).order_by("-datePub")

    paginated = paginate(posts, request, PublicationSerializer)

    return Response(paginated)
