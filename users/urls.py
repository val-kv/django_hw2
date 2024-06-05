from django.urls import path
from .views import CustomLoginView, reset_password, RegisterView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('reset_password/', reset_password, name='reset_password'),
]