from django.urls import path
from .views import CreateUserView, AuthCookieView, SessionView, LogoutView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name="register"),
    path('auth/login/', AuthCookieView.as_view(), name="get_token"),
    path('auth/session/', SessionView.as_view(), name="refresh"),
    path('auth/logout/', LogoutView.as_view(), name="logout")
]