from django.urls import path
from . import views

urlpatterns = [
    path('', views.WallHome.as_view(), name='home'),
    path('addpage/', views.AddPost.as_view(), name='add_page'),
    path('post/<slug:post_slug>', views.ShowPost.as_view(), name='post')
]
