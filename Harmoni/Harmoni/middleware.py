from django.utils.deprecation import MiddlewareMixin


class RefreshTokenMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        request_id = id(request)  # Get unique ID for this request object
        path = getattr(request, 'path', 'unknown')
        
        print(f"[MIDDLEWARE-{request_id}] [{path}] Checking for new access token...")
        
        # Check all attributes on request for debugging
        request_attrs = [attr for attr in dir(request) if 'token' in attr.lower()]
        print(f"[MIDDLEWARE-{request_id}] [{path}] Request attributes with 'token': {request_attrs}")
        
        new_access = getattr(request, "_new_access_token", None)
        print(f"[MIDDLEWARE-{request_id}] [{path}] new_access_token = {new_access[:50] + '...' if new_access else None}")
        
        if new_access:
            print(f"[MIDDLEWARE-{request_id}] [{path}] new access token detected... setting cookie")
            response.set_cookie(
                key="access_token",
                value=new_access,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=60*15,
            )
            print(f"[MIDDLEWARE-{request_id}] [{path}] Cookie set successfully")
        else:
            print(f"[MIDDLEWARE-{request_id}] [{path}] No new access token to set")
        
        return response