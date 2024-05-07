from django.contrib.auth import authenticate, login, logout

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        errors = {
            "not_found_user": "Bunday foydalanuvchi toplmadi!",
            "not_login": "Taqdim qilingan ma'lumotlar bilan tizimga kirib bo'lmadi !"
        }
        data = request.data
        
        phone_number = data.get("phone_number", None)
        password = data.get("password", None)
        if phone_number and password:
            user = authenticate(phone_number = phone_number, password = password)
            if user:
                token,_ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({
                    "phone_number": phone_number,
                    "token": token.key
                })
            else:
                return Response({
                    "error": errors['not_found_user']
                })
        else:
            return Response({
                "error": errors['not_login']
            })


class LogoutApi(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)

