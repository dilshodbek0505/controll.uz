from django.urls import path
from .views import (
    LoginApi,
    LogoutApi,
)

urlpatterns = [
    path('login/', LoginApi.as_view()),
    path('logout/', LogoutApi.as_view())
]
