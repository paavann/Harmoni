from rest_framework.permissions import BasePermissions
from rest_framework_simplejwt.tokens import AccessToken

class CookieJWTPermission(BasePermissions):
    def check_permission(self, request, view):
        token = request.COOKIES.get("access_token")
        if not token:
            return False
        try:
            AccessToken(token)
            return True
        except:
            return False