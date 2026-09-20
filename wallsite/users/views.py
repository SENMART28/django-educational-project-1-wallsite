from django.contrib.auth import get_user_model, user_logged_in
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.urls import reverse_lazy
from .forms import LoginUserForm, RegisterUserForm, UserPasswordChangeForm
from .utils import TitleMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginUser(LoginView, TitleMixin):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    title_page = 'Авторизация'
       
    
    def get_success_url(self):
        return reverse_lazy('wallapp:home')
    

class RegisterUser(CreateView, TitleMixin):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    title_page = 'Регистрация'


class ProfileUser(DetailView, LoginRequiredMixin, TitleMixin):
    model = get_user_model()
    template_name = 'users/profile.html'
    title_page = 'Профиль пользователя'
    pk_url_kwarg = 'user_id'
    pk_field = 'id'
    context_object_name = 'user'
    
    
class UserPasswordChange(PasswordChangeView, LoginRequiredMixin):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
    
    
class UserPosts(ListView, TitleMixin):
    context_object_name = 'posts'
    template_name = 'users/index.html'
    title_page = 'Посты пользователя'
    paginate_by = 2
    
    def get_queryset(self):
        return get_user_model().objects.get(pk=self.kwargs.get('user_id')).posts.filter(private=False)
    

class ChangeProfile(UpdateView, LoginRequiredMixin, TitleMixin):
    model = get_user_model()
    fields = ['username', 'first_name', 'last_name', 'photo']
    template_name = 'users/profile_change.html'
    title_page = 'Редактировать профиль'
    success_url = reverse_lazy('wallapp:home')
    
    def get_object(self, queryset=None):
        return self.request.user