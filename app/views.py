from django.shortcuts import render
from rest_framework import generics ,permissions
from .serializers import *
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login

class register(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = Response({
        "user": user_serializer(user, context=self.get_serializer_context()).data,
        })
        return response

class logine(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        response = super(logine, self).post(request, format=None)
        response.set_cookie("login_token",response.data["token"],path="/",max_age=3600*24*365,samesite='Lax')
        response.data['id'] = user.id
        return response