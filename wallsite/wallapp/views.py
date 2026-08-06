from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, ListView
from .models import Wall
from .utils import DataMixin
from .forms import AddPostForm
from django.contrib.auth.mixins import LoginRequiredMixin

class WallHome(DataMixin, ListView):
    template_name = 'wall/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    
    def get_queryset(self):
        return Wall.objects.all().select_related('author')
    

class AddPost(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'wall/add_page.html'
    title_page = 'Создать пост'
    
    def form_valid(self, form):
        w = form.save(commit=False)
        if self.request.user:
            w.author = self.request.user
        return super().form_valid(form)
    
class ShowPost(DataMixin, DetailView):
    model = Wall
    template_name = 'wall/show_post.html'
    slug_url_kwarg = 'post_slug'
    slug_field = 'slug'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title_page'] = context['post'].title
        return context