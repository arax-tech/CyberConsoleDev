from django.urls import path
from authentication.views import UserLoginView, UserRegistrationView, UserProfileView, UserUpdatePasswordView, SendPasswordResetEmailView, UserPasswordResetView, UserUpdateProfileView, SendPasswordUpdateEmailView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile_update"),
    path("profile_update/", UserUpdateProfileView.as_view(), name="profile"),
    path("update_password/", UserUpdatePasswordView.as_view(), name="update_password"),
    path("send-reset-password-email/", SendPasswordResetEmailView.as_view(), name="send-reset-password-email"),
    path("reset-password/<uid>/<token>/", UserPasswordResetView.as_view(), name="reset-password"),
    path("send-update-password-email/", SendPasswordUpdateEmailView.as_view(), name="send-update-password-email"),
]
