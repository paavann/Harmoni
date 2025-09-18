from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        request_id = id(request)  # Get unique ID for this request object
        path = getattr(request, 'path', 'unknown')
        
        access_token = request.COOKIES.get("access_token")
        print(f"[REQ-{request_id}] [{path}] access_token: {access_token}")
        refresh_token = request.COOKIES.get("refresh_token")
        print(f"[REQ-{request_id}] [{path}] refresh_token: {refresh_token}")

        try:
            validated_token = self.get_validated_token(access_token)
            print(f"[REQ-{request_id}] [{path}] Access token is valid, using it")
            return self.get_user(validated_token), validated_token
        except Exception as e:
            print(f"[REQ-{request_id}] [{path}] Access token validation failed: {e}")
            print(f"[REQ-{request_id}] [{path}] access token doesn't exist. attempting to refresh...")
            if not refresh_token:
                print(f"[REQ-{request_id}] [{path}] No refresh token available")
                return None
            try:
                refresh = RefreshToken(refresh_token)
                new_access_str = str(refresh.access_token)
                new_access_token = AccessToken(new_access_str)
                print(f"[REQ-{request_id}] [{path}] Generated new access token: {new_access_str[:50]}...")
                
                user = self.get_user(new_access_token)
                print(f"[REQ-{request_id}] [{path}] Got user from new access token: {user.email if hasattr(user, 'email') else user}")
                
                # Set the new token
                request._new_access_token = new_access_str
                print(f"[REQ-{request_id}] [{path}] Set _new_access_token on request")
                
                # Double check it was set
                check_token = getattr(request, '_new_access_token', 'NOT_FOUND')
                print(f"[REQ-{request_id}] [{path}] Verification - _new_access_token: {check_token[:50] + '...' if check_token != 'NOT_FOUND' else 'NOT_FOUND'}")
                
                return user, new_access_token
            except Exception as e:
                print(f"[REQ-{request_id}] [{path}] Refresh token validation failed: {e}")
                return None