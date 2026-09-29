from django.urls import path
from . import views

app_name = 'wallapp'

urlpatterns = [
    path('', views.WallHome.as_view(), name='home'),
    path('addpage/', views.AddPost.as_view(), name='add_page'),
    path('post/<slug:post_slug>', views.ShowPost.as_view(), name='post'),
    path('post/<slug:post_slug>/like', views.ToggleLike, name='togglelikepost'),
    path('post/delete/<slug:post_slug>', views.DeletePost.as_view(), name='delete_post'),
    path('post/owner_delete/<slug:post_slug>', views.OwnerDeletePost.as_view(), name='owner_delete_post'),
    path('comment/delete/<int:comment_pk>', views.DeleteComment.as_view(), name='delete_comment'),
    path('comment/owner_delete/<int:comment_pk>', views.OwnerDeleteComment.as_view(), name='owner_delete_comment'),
]
