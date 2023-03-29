from django.urls import path
from .views import *

app_name = "testapp"

urlpatterns = [
    path("home/", HomePageView.as_view(), name="home"),
    path("signup/", ClientRegisterationView.as_view(), name="signup"),
    path("login/", ClientLoginView.as_view(), name="login"),
    path("logout/", ClientLogoutView.as_view(), name="logout"),
    path("forgot-password/", ForgetPasswordView.as_view(), name="forgot_password"),
    path("reset-password/<email>/<token>/", ResetPasswordView.as_view(), name="reset_password"),
    path('change-password/<int:pk>/',ChangePasswordView.as_view() , name="change_password"),
    path("profile/", ClinetProfileView.as_view(), name="client_profile"),
    path("update-profile/<int:pk>/", UpdateClientProfileView.as_view(), name="update_profile")
]