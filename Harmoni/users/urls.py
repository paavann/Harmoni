from django.urls import path
from .views import CreateUserView, AuthCookieView, SessionView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name="register"),
    path('auth/login/', AuthCookieView.as_view(), name="get_token"),
    path('auth/session/', SessionView.as_view(), name="refresh"),
]