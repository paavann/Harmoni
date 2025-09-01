from .models import User
from .serializers import UserSerializer

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status



class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            "message": "Login Successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "mbti_type": user.mbti_type
            }
        }, status=status.HTTP_201_CREATED)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60*15
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60*60*24*7
        )
        return response


class AuthCookieView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({ "detail": "Invalid credentials" })

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            "message": "Login Successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "mbti_type": user.mbti_type
            }
        })
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60*15
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60*60*24*7
        )

        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response(
            { "message": "logout successful" },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value="",
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=0,
        )
        response.set_cookie(
            key="refresh_token",
            value="",
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=0,
        )

        return response


class RefreshCookieView(APIView):
    permission_classes = [AllowAny] #access_token is invalid.

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({ "detail": "no refresh token" }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            response = Response({ "message": "token refreshed" })
            response.set_cookie(
                key="access_token",
                value=new_access,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=60*15
            )
            return response
        except:
            return Response({ "detail": "invalid refresh token" }, status=status.HTTP_401_UNAUTHORIZED)
        

class SessionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if not access_token and not refresh_token:
            return Response(
                { "message": "not authenticated" },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            access = AccessToken(access_token)
            user = User.objects.get(id=access["user_id"])
            serialized_user = UserSerializer(user)

            return Response({ "user": serialized_user.data }, status=status.HTTP_200_OK)
        except Exception:
            if not refresh_token:
                return Response({ "message": "no valid token" }, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                refresh = RefreshToken(refresh_token)
                new_access = str(refresh.access_token)

                user = User.objects.get(id=refresh["user_id"])
                serialized_user = UserSerializer(user)

                response = Response({ "user": serialized_user.data }, status=status.HTTP_200_OK)
                response.set_cookie(
                    key="access_token",
                    value=new_access,
                    httponly=True,
                    secure=False,
                    samesite="Lax",
                    max_age=60*15,
                )

                return response
            except Exception:
                return Response({ "message": "invalid refresh token" }, status=status.HTTP_401_UNAUTHORIZED)
            