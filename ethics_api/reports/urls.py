# reports/urls.py
from .views_auth import RequestOTPView, VerifyOTPView
from .views import ReportView
from django.urls import path

urlpatterns = [
        path('auth/verify-otp/', VerifyOTPView.as_view()),
    path('report/', ReportView.as_view()),
]