from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.utils import paginate
from ..models import College, CollegeUser, User
from ..permissions import IsCollegeAdmin
from ..sub_serializers.user_serializer import UserSerializer
from ..sub_serializers.college_serializer import CollegeSerializer, CollegeUserSerializer
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from ..utils import getFromModel
from django.db.models import Q


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
    college = getFromModel(College, pk)

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
def list_request(request: Request):
    name = request.query_params.get("name")

    college = request.user.college

    if name:
        users_requested = CollegeUser.objects.filter(
            Q(college=college, isConfirmed=False) &
            Q(Q(user__first_name__icontains=name) | Q(user__last_name__icontains=name))
        ).order_by("dateRequested")

    else:
        users_requested = CollegeUser.objects.filter(college=college, isConfirmed=False).order_by("dateRequested")

    response = paginate(users_requested, request, CollegeUserSerializer)

    return Response(response)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsCollegeAdmin])
def take_action_to_request(request: Request, pk):
    #     pk is the primary key of the request

    userRequested = CollegeUser.objects.filter(pk=pk).first()

    if not userRequested:
        return Response("request not found", status=status.HTTP_404_NOT_FOUND)

    # action: accept, refuse (by default,it's accept)
    action = request.query_params.get("action") if request.query_params.get("action") else "accept"

    confirmation = action == "accept"

    userRequested.isConfirmed = confirmation

    userRequested.save()

    return Response(CollegeUserSerializer(userRequested).data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def college_detail(request:Request, pk):
    college = getFromModel(College, pk)

    return Response(CollegeSerializer(college).data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def enrolled_college(request:Request):
    user = request.user

    # if he is an admin
    if user.isAdminCollege:
        college= [user.college]

    else:
        college_id = CollegeUser.objects.filter(user=user, isConfirmed=True).values("college").distinct()

        college = College.objects.filter(id__in=college_id)

    paginated = paginate(college, request, CollegeSerializer)

    return Response(paginated)