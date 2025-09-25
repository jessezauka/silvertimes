from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView,
    PasswordResetDoneView, PasswordResetCompleteView
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .forms import RegisterForm

UserModel = get_user_model()

class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Ensure session login even if we didn't call authenticate()
            backend = getattr(
                settings,
                'AUTHENTICATION_BACKENDS',
                ['django.contrib.auth.backends.ModelBackend']
            )[0]
            login(request, user, backend=backend)

            # Honor ?next=; otherwise use LOGIN_REDIRECT_URL or '/'
            next_url = (
                request.GET.get('next')
                or request.POST.get('next')
                or getattr(settings, 'LOGIN_REDIRECT_URL', '/')
            )
            messages.success(request, 'Welcome! Your account was created.')
            return redirect(next_url)

        # Surface validation errors during development
        try:
            print("REGISTER ERRORS:", form.errors.as_json())
        except Exception:
            pass

        messages.error(request, 'Please fix the errors below.')
        return render(request, self.template_name, {'form': form})


class SignInView(LoginView):
    template_name = 'registration/login.html'
    # On success, LoginView uses settings.LOGIN_REDIRECT_URL or ?next=


class SignOutView(LogoutView):
    next_page = reverse_lazy('home')  # or settings.LOGOUT_REDIRECT_URL


class ResetPasswordView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.txt'
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

@method_decorator(login_required, name='dispatch')
class AccountView(TemplateView):
    template_name = 'registration/account.html'