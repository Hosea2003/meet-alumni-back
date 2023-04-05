from rest_framework.decorators import api_view, permission_classes
from api.utils import paginate
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from people.models import Friend, FriendRequest
from people.serializer import PublicUserSerializer, RequestSerializer, PublicCollegeUserSerializer
from user.models import User, College, CollegeUser
from user.utils import getFromModel
from rest_framework import status


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_friends(request: Request):
    user = request.user
    friends = Friend.objects.filter(user1=user).values("user2")
    friends= User.objects.filter(id__in=friends)

    paginated = paginate(friends, request, PublicUserSerializer)
    return Response(paginated)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_friends_request(request: Request):
    user = request.user

    requests = FriendRequest.objects.filter(friend=user).order_by("-dateRequest").values("sender")

    requests = User.objects.filter(id__in=requests)

    paginated = paginate(requests, request, PublicUserSerializer)

    return Response(paginated)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def send_request(request: Request, pk):
    user = request.user

    # check if it's the same connected person
    if pk == user.id:
        return Response("You can't send request to yourself")

    other_user = getFromModel(User, pk)

    #     check if the user has already sent a request to this person

    request_count = FriendRequest.objects.filter(sender=user, friend=other_user).count()

    if request_count > 0:
        return Response("You already sent a request to this person")

    FriendRequest.objects.create(
        sender=user,
        friend=other_user
    )

    return Response(PublicUserSerializer(other_user, context={"request":request}).data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def accept_friend(request, pk):
    sender = getFromModel(User, pk)
    user = request.user
    request_to_me = FriendRequest.objects.filter(sender=sender, friend=user).first()

    if not request_to_me:
        return Response("This person didn't send you a request", status=status.HTTP_400_BAD_REQUEST)

#     create 2 Friend objects (me as user1 and as user2)
    Friend.objects.create(
        user1=user,
        user2=sender
    )

    Friend.objects.create(
        user1=sender,
        user2=user
    )

#     delete the request
    request_to_me.delete()

    return Response(PublicUserSerializer(sender, context={"request":request}).data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_college_member(request: Request, pk):
    college = getFromModel(College, pk)

    searchIn = request.query_params.get("search") if request.query_params.get("search") else "all"

    if searchIn == "all":
        members = CollegeUser.objects.filter(college=college, isConfirmed=True)

    elif searchIn == "student":
        members = CollegeUser.objects.filter(college=college, isConfirmed=True, isAlumni=False)

    else:
        members = CollegeUser.objects.filter(college=college, isConfirmed=True, isAlumni=True)

    members = members.exclude(user=request.user)

    paginated = paginate(members, request, PublicCollegeUserSerializer)

    return Response(paginated)
