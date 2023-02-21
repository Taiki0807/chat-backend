from django.urls import path, include
from rest_framework import routers
from .views import TokenObtainView,TokenDeleteView,TokenRefreshView,AccountRegister,GetAccountInfo,refresh_get

urlpatterns = [
    path('register/', AccountRegister.as_view()),
    path('get/', GetAccountInfo.as_view()),
    path('login/', TokenObtainView.as_view()),
    path('logout/', TokenDeleteView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('refresh-token/', refresh_get),
]