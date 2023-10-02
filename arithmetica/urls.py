from django.urls import path

from .views import *

urlpatterns = [
    path("user-info/create/", UserInfoCreateView.as_view()),
    path("user-info/<int:pk>/",UserInfoRetriveUpdateDestroyView.as_view() ),
    path("round-info/create/", RoundInfoCreateView.as_view()),
    path("round-info/<int:round_number>/",RoundInfoRetriveUpdateDestroyView.as_view() ),
    path("error-info/create/", ErrorInfoCreateView.as_view()),
    path("error-info/<int:round>/",ErrorInfoRetriveUpdateDestroyView.as_view() ),
]
