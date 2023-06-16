from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from authentication.renderers import UserRenderer
from authentication.serializers import UserLoginSerializer, UserRegistrationSerializer, UserProfileSerializer, UserUpdatePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer, UserUpdateProfileSerializer, SendPasswordUpdateEmailSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from rest_framework.parsers import MultiPartParser, FormParser



# Generate Auth Token 
def get_auth_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        # 'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_auth_token(user)
            return Response({"status" : 201, "message": "Registration Successfully...", "token" : token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_auth_token(user)
                return Response({'status' : 203, 'message' : "Login Successfully...", "token" : token}, status=status.HTTP_200_OK)
            else :
                return Response({'status' : 404, 'message' : "Invalid Email or Password..."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({"user" : serializer.data}, status=status.HTTP_200_OK)

class UserUpdateProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  parser_classes = [MultiPartParser, FormParser]

  def post(self, request, format=None):
    serializer = UserUpdateProfileSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'status' : 200, 'message' : "Profile Update Successfully..."}, status=status.HTTP_200_OK)
      
class UserUpdatePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserUpdatePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'status' : 200, 'message' : "Password Update Successfully..."}, status=status.HTTP_200_OK)
  

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'status' : 200, 'message' : "Password Reset link send. Please check your Email..."}, status=status.HTTP_200_OK)

class SendPasswordUpdateEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordUpdateEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'status' : 200, 'message' : "Password Update Link. Please check your Email..."}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,uid,token,format=None,):
        serializer = UserPasswordResetSerializer(data=request.data,context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'status': 200,'message': 'Password Reset Successfully...'},status=status.HTTP_200_OK)
