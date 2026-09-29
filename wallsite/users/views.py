from multiprocessing import get_context

from django.contrib.auth import get_user_model, user_logged_in
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.urls import reverse_lazy
from .forms import LoginUserForm, RegisterUserForm, UserPasswordChangeForm
from .utils import TitleMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class LoginUser(TitleMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    title_page = 'Авторизация'
       
    
    def get_success_url(self):
        return reverse_lazy('wallapp:home')
    

class RegisterUser(TitleMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    title_page = 'Регистрация'


class ProfileUser(LoginRequiredMixin, TitleMixin, DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    title_page = 'Профиль пользователя'
    pk_url_kwarg = 'user_id'
    pk_field = 'id'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user_model().objects.get(pk=self.kwargs.get('user_id'))
        context['user_can_delete_wall'] = user.has_perm('wallapp.delete_wall')
        context['user_can_delete_comment'] = user.has_perm('wallapp.delete_comment')
        return context
    
    
class UserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
    
    
class UserPosts(TitleMixin, ListView):
    context_object_name = 'posts'
    template_name = 'users/posts_list.html'
    title_page = 'Посты пользователя'
    paginate_by = 5
    
    def get_queryset(self):
        return get_user_model().objects.get(pk=self.kwargs.get('user_id')).posts.select_related('author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_can_delete_wall'] = self.request.user.has_perm('wallapp.delete_wall')
        return context
    

class UserComments(TitleMixin, ListView):
    context_object_name = 'comments'
    template_name = 'users/comments_list.html'
    title_page = 'Комментарии пользователя'
    paginate_by = 5
    
    def get_queryset(self):
        return get_user_model().objects.get(pk=self.kwargs.get('user_id')).comments.select_related('author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_can_delete_comment'] = self.request.user.has_perm('wallapp.delete_comment')
        return context
    

class ChangeProfile(LoginRequiredMixin, TitleMixin, UpdateView):
    model = get_user_model()
    fields = ['username', 'first_name', 'last_name', 'photo']
    template_name = 'users/profile_change.html'
    title_page = 'Редактировать профиль'
    success_url = reverse_lazy('wallapp:home')
    
    def get_object(self, queryset=None):
        return self.request.user