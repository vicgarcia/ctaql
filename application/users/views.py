from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_jwt.views import ObtainJSONWebToken, jwt_response_payload_handler
from users.models import User
from users.authentication import JSONWebTokenAuthentication, IsAuthenticated
from .serializers import ProfileSerializer


class LoginView(ObtainJSONWebToken):
    """
        override the post method of ObtainJSONWebToken to populate the last_login field
    """

    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            data = jwt_response_payload_handler(token, user, request)
            user.update_last_login()
            return Response(data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
        api to manage a user account

        allow user to update email and password
    """

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = ProfileSerializer(instance=request.user)
        return Response(serializer.data, status=HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serializer = ProfileSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

