from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from .serializers import SignupSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
# Create your views here.

class SignupView(generics.GenericAPIView):
  serializer_class = SignupSerializer
  permission_classes = [AllowAny]


  def post(self, request:Request):
    data_incoming = request.data
    serializer = self.serializer_class(data= data_incoming)

    if serializer.is_valid():
      response = {"Message": "Signup was successful",
                  "User": serializer.data}
      
      serializer.save()

      return Response(data=response, status=status.HTTP_202_ACCEPTED)
    
    return Response(data=serializer.errors)
  


class LoginView(APIView):
  permission_classes = [AllowAny]
  
  def post(self, request:Request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)

    if user is not None:
      response = {"Message": "Login Succesful",
                 "Token": user.auth_token.key}
      response2 = {"Message": "Login Failed \n Check credentials"}
      
      return Response(data=response, status=status.HTTP_202_ACCEPTED)
    return Response(data=response2, status=status.HTTP_400_BAD_REQUEST)
  

  def get(self, request:Request):
    content = {
      "User": str(request.user),
      "auth": str(request.auth)
    }

    return Response(data=content, status=status.HTTP_200_OK)


    


