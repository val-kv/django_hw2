from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.views import FormView
from django.views.generic import CreateView
from catalog.models import Product
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random
import string


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = '/login/'

    def form_valid(self, form):
        user = form.save()
        send_mail(
            'Подтверждение почты',
            'Пожалуйста, подтвердите свою почту, перейдя по ссылке.',
            'val-kv2008@yandex.ru',  # Отправитель
            [user.email],  # Получатель
            fail_silently=False,
        )
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'registration/reset_password.html', {'error': 'Пользователь с такой почтой не найден.'})

        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Генерация нового пароля
        user.password = make_password(new_password)  # Установка захешированного нового пароля
        user.save()

        # Отправка письма с новым паролем на адрес пользователя
        # Для отправки писем используйте send_mail() как в предыдущем примере
        return render(request, 'registration/reset_password.html', {'message': 'Новый пароль отправлен на вашу почту.'})
    else:
        return render(request, 'registration/reset_password.html')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)