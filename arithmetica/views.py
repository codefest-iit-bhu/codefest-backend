from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, authentication
from rest_framework.views import APIView
from .models import *


# Create your views here.
class UserInfoCreateView(generics.CreateAPIView):
    http_method_names = ["post"]
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def perform_create(self, serializer):
        id = User.objects.get(username=self.request.user)
        serializer.save(user=id)
        return serializer.validated_data


class UserInfoRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    lookup_field = "pk"

    def get_queryset(self):
        return UserInfo.objects.filter(id=self.kwargs.get("pk"))

    def perform_update(self, serializer):
        id = User.objects.get(username=self.request.user)
        serializer.save(user=id)
        return serializer.validated_data


class RoundInfoCreateView(generics.CreateAPIView):
    http_method_names = ["post"]
    serializer_class = RoundInfoSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.validated_data


class RoundInfoRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoundInfoSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    lookup_field = "round_number"

    def get_queryset(self):
        return RoundInfo.objects.filter(round_number=self.kwargs.get("round_number"))

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.validated_data

class ErrorInfoCreateView(generics.CreateAPIView):
    http_method_names = ["post"]
    serializer_class = ErrorInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        round_number=self.request.data.get("round_number")
        round=RoundInfo.objects.get(round_number=round_number)
        u_info=UserInfo.objects.get(user=self.request.user)
        serializer.save(user_info=u_info,round=round_number)
        return serializer.validated_data


class ErrorInfoRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ErrorInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    
    lookup_field="round"
    def get_queryset(self):
        return ErrorInfo.objects.filter(round__round_number=self.kwargs.get("round"),user_info__user=self.request.user)

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.validated_data
