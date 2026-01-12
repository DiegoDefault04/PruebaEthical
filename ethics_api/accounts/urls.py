from django.urls import path
from .views import RegisterView, LoginStepOneView, VerifyOTPView

urlpatterns = [
    path("login/", LoginStepOneView.as_view()),
    path("verify/", VerifyOTPView.as_view()),
]

