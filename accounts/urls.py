from django.urls import path
from .views import (
    AccountView, RegisterView, SignInView, SignOutView,
    ResetPasswordView, ResetPasswordDoneView,
    ResetPasswordConfirmView, ResetPasswordCompleteView,
)

app_name = 'accounts'

urlpatterns = [
    path('account/', AccountView.as_view(), name='account'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',    SignInView.as_view(),  name='login'),
    path('logout/',   SignOutView.as_view(), name='logout'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset/done/', ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', ResetPasswordCompleteView.as_view(), name='password_reset_complete'),
]
