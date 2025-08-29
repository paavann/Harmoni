from django.urls import path
from .views import CreateUserView, AuthCookieView, RefreshCookieView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name="register"),
    path('auth/login/', AuthCookieView.as_view(), name="get_token"),
    path('auth/refresh/', RefreshCookieView.as_view(), name="refresh"),
]