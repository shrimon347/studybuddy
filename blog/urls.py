from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('airtcle/<str:slug>', views.detail, name='detail'),
   path('create-post/', views.create_blog, name='create'),
   path('update-post/<str:slug>', views.updatePost, name='update'),
   path('delete-post/<str:slug>', views.deletePost, name='delete'),
   path('delete-comment/<str:pk>/', views.deleteComment, name="delete-comment"),
   path('categorys/', views.categoryPage, name="categorys"),
   path('like/', views.like_post, name='like-post'),
]
