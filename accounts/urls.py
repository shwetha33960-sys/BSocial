from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("signin/", views.signin_view, name="signin"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("signout/", views.signout_view, name="signout"),
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path("edit-profile/", views.edit_profile_view, name="edit_profile"),
]
