from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from user.sub_serializers.user_serializer import UserSerializer


class MyTokenOtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        user_serializer = UserSerializer(user)

        for key in user_serializer.data.keys():
            token[key] = user_serializer.data[key]

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenOtainPairSerializer
