from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView
from .models import Wall
from .utils import TitleMixin
from .forms import AddCommentForm, AddPostForm
from django.contrib.auth.mixins import LoginRequiredMixin

class WallHome(TitleMixin, ListView):
    template_name = 'wall/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    paginate_by = 5
    
    def get_queryset(self):
        return Wall.objects.all().select_related('author').prefetch_related('likes', 'comments__author')
    

class AddPost(LoginRequiredMixin, TitleMixin, CreateView):
    form_class = AddPostForm
    template_name = 'wall/add_page.html'
    title_page = 'Создать пост'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class ShowPost(TitleMixin, DetailView):
    model = Wall
    template_name = 'wall/show_post.html'
    slug_url_kwarg = 'post_slug'
    slug_field = 'slug'
    context_object_name = 'post'
    title_page = 'Смотреть пост'
    
    def get_queryset(self):
        return Wall.objects.select_related('author').prefetch_related('comments__author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title_page'] = context['post'].title
        context['form'] = AddCommentForm()
        
        is_liked = False
        if self.request.user.is_authenticated:
            is_liked = self.object.likes.filter(pk=self.request.user.pk).exists()
        context['is_liked'] = is_liked
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect('users:login')
        
        form = AddCommentForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post = self.object
            form.save()
            
            return redirect(self.object.get_absolute_url())
        
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)
            
    

@login_required
@require_POST
def ToggleLike(request, post_slug):
    post = get_object_or_404(Wall, slug=post_slug)
    
    if request.user not in post.likes.all():
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)
        
    return redirect(request.META.get('HTTP_REFERER', reverse('wallapp:home')))