from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response
import rest_framework.status as status
from .models import User, College, CollegeUser, ProfilePicture

from .sub_serializers.user_serializer import UserSerializer, ProfilePictureSerializer
from .sub_serializers.college_serializer import CollegeSerializer
from .utils import getFromModel


@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def checkEmail(request:Request):
    email = request.query_params.get("email")

    if not email:
        return Response("Provide an email params", status=status.HTTP_400_BAD_REQUEST)

    user_with_email = User.objects.filter(email=email).count()

    return Response(user_with_email>0)


@api_view(["POST"])
def register(request):
    college_data = None

    if request.data.get("college"):
        college_data: dict = request.data.pop("college")

    user_data = request.data

    user_serializer = UserSerializer(data=user_data)

    if not user_serializer.is_valid():
        return Response(user_serializer.errors)

    user = User(
        email=user_data.get("email"),
        password=user_data.get("password"),
        first_name=user_data.get("first_name"),
        last_name=user_data.get("last_name"),
        address=user_data.get("address"),
        birthdate=user_data.get("birthdate"),
        gender=user_data.get("gender"),
        contact=user_data.get("contact")
    )

    user.save()

    # deal with the college data
    # add an option:do it later
    if not college_data:
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    # if it provides an id, test if it exists
    college_id = college_data.get("id")

    if college_id:
        college = College.objects.filter(id=college_id).first()
        if not college:
            return Response("College not found", status=status.HTTP_400_BAD_REQUEST)

        # create a relation between the user and the college
        # send at the same time a request to admin
        CollegeUser.objects.create(
            user=user,
            college=college,
            # by default, he is not an Alumni
            isAlumni=college_data.get("isAlumni") if college_data.get("isAlumni") else False
        )

    else:
        college_serializer = CollegeSerializer(data=college_data)
        if not college_serializer.is_valid():
            # delete the created user because some details are not valid
            user.delete()
            return Response(college_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        college = College(
            name=college_data.get("name"),
            website=college_data.get("website"),
            email=college_data.get("address"),
            contact=college_data.get("contact"),
            address=college_data.get("address"),
            admin=user
        )

        college.save()

    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test(request):
    user = request.user
    return Response(UserSerializer(user).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def change_profile_picture(request: Request):
    user = request.user

    # get the image from FormData (that's why we need a parser)
    serializer = ProfilePictureSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors)

    # change the previous profile picture into not current
    current_pf = ProfilePicture.objects.filter(user=user, isCurrent=True).first()

    if current_pf:
        current_pf.isCurrent = False

        current_pf.save()

    serializer.save(user=user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_details(request:Request, pk):
    user= getFromModel(User, pk)

    return Response(UserSerializer(user).data)
