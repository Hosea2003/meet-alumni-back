from django.contrib.auth.hashers import make_password
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.utils import paginate
from people.serializer import PublicUserSerializer
from user.models import User
from user.sub_serializers.user_serializer import UserProfileSerializer, ProfilePictureSerializer, \
    UpdateUserInfoSerializer, UserSerializer
from user.utils import getFromModel
from people.models import Friend


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def about(request: Request, pk):
    user = getFromModel(User, pk)

    return Response(UserProfileSerializer(user).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def friends(request: Request, pk):
    user = getFromModel(User, pk)
    friend = Friend.objects.filter(user1=user).values("user2")
    friend = User.objects.filter(id__in=friend)

    paginated = paginate(friend, request, PublicUserSerializer)

    return Response(paginated)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def album(request: Request, pk):
    user: User = getFromModel(User, pk)
    profile_pictures = user.profile_pictures.all()
    paginated = paginate(profile_pictures, request, ProfilePictureSerializer)
    return Response(paginated)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_info(request:Request):
    user=request.user
    serializer=UpdateUserInfoSerializer(user,data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors)

    serializer.save()

    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request:Request):
    user=request.user
    password=request.data.get("password")
    old_password = request.data.get("old_password")

    if not (password or old_password):
        return Response(False)

    if not user.check_password(old_password):
        return Response(False)

    user.set_password(password)
    user.save()

    return Response(True)