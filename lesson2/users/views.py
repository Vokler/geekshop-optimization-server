from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import CommonContextMixin
from users.common import get_user_location
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(CommonContextMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'

    def form_valid(self, form):
        user = form.get_user()
        location = get_user_location(self.request)
        user.update_or_create_location(**location)
        return super(UserLoginView, self).form_valid(form)


class UserRegistrationView(CommonContextMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегестрировались! Письмо с подтверждением отправлено на вашу почту'
    title = 'GeekShop - Регистрация'


class UserProfileView(CommonContextMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'GeekShop - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class UserEmailVerification(CommonContextMixin, TemplateView):
    title = 'GeekShop - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.last().is_expired():
            user.is_verified_email = True
            user.save()
            return super(UserEmailVerification, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('index'))
