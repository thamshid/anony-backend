from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from anony_app.base_response import HttpSuccessResponse, HttpErrorResponse
from anony_app.models import User, Message
from anony_app.serializers import UserDetailedSerializer, MessageSerializer


class AuthenticationView(CreateAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        API for Login
        ---
        - code: 200
          message: Login successful
        - code: 401
          message: Invalid Credentials
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = UserDetailedSerializer(user)
            return HttpSuccessResponse({'token': token.key, 'user': user_serializer.data}, 'Login Success')
        else:
            return HttpErrorResponse('Login Fail', status.HTTP_401_UNAUTHORIZED)


class SignUp(CreateAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = UserDetailedSerializer
    queryset = User.objects.all()


class MessageCreate(CreateAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class MessageListCreate(ListAPIView):
    throttle_classes = ()
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

