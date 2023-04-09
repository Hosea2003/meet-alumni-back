from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from api.utils import paginate
from message.models import Message
from message.serializer import MessageSerializer, MessageUserSerializer
from people.models import Friend
from user.models import User
from django.db.models import Q
from django.utils import timezone

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request:Request, pk):
    receiver=get_object_or_404(User, pk=pk)
    user = request.user
    message = request.data.get("message")

    if not message:
        return Response("Provide message")

    message = Message.objects.create(
        sender=user,
        receiver=receiver,
        content=message
    )

    return Response(MessageSerializer(message).data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_message(request, pk):
    user = get_object_or_404(User, pk=pk)
    messages=Message.objects.filter(Q(
        Q(sender=user, receiver=request.user)|
        Q(sender=request.user, receiver=user))).order_by("-dateSend")

    paginated = paginate(messages, request, MessageSerializer)

    return Response(paginated)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_last_message(request:Request):
    user = request.user
    friends = Friend.objects.filter(user1=user)

    last_message=[]

    for friend in friends:
        message = Message.objects.filter(Q(
            Q(sender=user, receiver=friend.user2)|
            Q(sender=friend.user2, receiver=user)
        )).order_by("-dateSend").first()

        if not message:
            last_message.append({
                "friend":friend.user2,
                "content":"You can send message to your friend",
                "dateSend":timezone.now(),
                "lastSenderMe":False
            })

        else:
            last_message.append({
                "friend":friend.user2,
                "content":message.content,
                "dateSend":message.dateSend,
                "lastSenderMe":message.sender.id==user.id
            })


    paginated = paginate(last_message, request, MessageUserSerializer)

    return Response(paginated)