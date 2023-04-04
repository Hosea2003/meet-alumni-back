from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from ..models import College, CollegeUser, User
from ..permissions import IsCollegeAdmin
from ..sub_serializers.user_serializer import UserSerializer
from ..sub_serializers.college_serializer import CollegeSerializer, CollegeUserSerializer
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from ..utils import getFromModel




@api_view(["GET"])
def list_colleges(request: Request):
    name = request.query_params.get("name")

    colleges = College.objects.all()

    if name:
        colleges = colleges.filter(name__icontains=name)

    return Response(CollegeSerializer(colleges, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_request_to_college(request: Request, pk):
    # get the primary key in the url
    college = getFromModel(College,pk)

    user = request.user

    isAlumni = request.data.get("isAlumni")

    if not isAlumni:
        return Response({"error_message": "isAlumni is required"})

    # save an object of collegeUser
    CollegeUser.objects.create(
        user=user,
        college_id=pk,
        isAlumni=isAlumni
    )

    return Response(CollegeSerializer(college).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsCollegeAdmin])
def list_request(request):
    college = request.user.college
    usersRequested = CollegeUser.objects.filter(college=college, isConfirmed=False).order_by("dateRequested")

    return Response(CollegeUserSerializer(usersRequested, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsCollegeAdmin])
def take_action_to_request(request: Request, pk):
    #     pk is the primary key of the request

    userRequested = CollegeUser.objects.filter(pk=pk).first()

    if not userRequested:
        return Response("request not found", status=status.HTTP_404_NOT_FOUND)

    # action: accept, refuse (by default,it's accept)
    action = request.query_params.get("action") if request.query_params.get("action") else "accept"

    confirmation = action=="accept"

    userRequested.isConfirmed=confirmation

    userRequested.save()

    return Response(CollegeUserSerializer(userRequested).data, status=status.HTTP_200_OK)