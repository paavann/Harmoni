from django.utils.deprecation import MiddlewareMixin


class RefreshTokenMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        new_access = getattr(request, "_new_access_token", None)
        if new_access:
            print("refresh triggered!")
            response.set_cookie(
                key="access_token",
                value=new_access,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=60*15,
            )
        return response