from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from .forms import LoginUserForm, RegisterUserForm, UserPasswordChangeForm
from .utils import DataMixin


class LoginUser(LoginView, DataMixin):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    title_page = 'Авторизация'
       
    
    def get_success_url(self):
        return reverse_lazy('wallapp:home')
    

class RegisterUser(CreateView, DataMixin):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    title_page = 'Регистрация'


class ProfileUser(DetailView, DataMixin):
    model = get_user_model()
    template_name = 'users/profile.html'
    title_page = 'Личный профиль'
    
    def get_object(self):
        return self.request.user
    
    
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'