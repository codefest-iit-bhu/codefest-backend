from django.urls import path, re_path

from .views import *

urlpatterns = [
    path("user-info/create/", UserInfoCreateView.as_view()),
    re_path(r'^user-info/(?P<pk>\d+)?/?$', UserInfoRetriveUpdateDestroyView.as_view(), name='userinfo-detail'),
    path("round-info/create/", RoundInfoCreateView.as_view()),
    path("round-info/<int:round_number>/",RoundInfoRetriveUpdateDestroyView.as_view() ),
    path('round-info/public/', RoundInfoPublicView.as_view(), name='round-info-list-create'),
    path("round-info/public/<int:round_number>/",RoundInfoPublicView.as_view() ),
    path("error-info/create/", ErrorInfoCreateView.as_view()),
    path("error-info/<int:round>/",ErrorInfoRetriveUpdateDestroyView.as_view() ),
    path('calculate_error/', CalculateErrorView.as_view(), name="calculate_error"),
    path('calculate_credits/', DeductCreditsView.as_view(), name="calculate_credits"),
]
