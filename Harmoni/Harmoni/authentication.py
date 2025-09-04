from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        print("access_token: ", access_token)
        refresh_token = request.COOKIES.get("refresh_token")
        print("refresh_token: ", refresh_token)

        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        except Exception:
            if not refresh_token:
                return None
            try:
                refresh = RefreshToken(refresh_token)
                new_access_str = str(refresh.access_token)
                new_access_token = AccessToken(new_access_str)
                user = self.get_user(refresh)
                request._new_access_token = new_access_str
                return user, new_access_token
            except:
                return None