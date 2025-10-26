from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ProfileView, RegisterView, EmailTokenObtainPairView, GuestLoginView, ForgotPasswordView, ResetPasswordView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("guest/", GuestLoginView.as_view(), name="guest_login"),
    path("password/forgot/", ForgotPasswordView.as_view(), name="password_forgot"),
    path("password/reset/", ResetPasswordView.as_view(), name="password_reset"),
]
