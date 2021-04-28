from django.urls import path
from . import views

urlpatterns = [
    path(r'<str:section>/article-<int:article_id>', views.articles_view, name='article_view'),
    path('create_article/', views.create_article_view, name='create_article'),
    path(r'<str:section>/article-<int:article_id>/update/', views.update_article_view, name='update_article'),
    path(r'<str:section>/article-<int:article_id>/delete/', views.delete_article_view, name='delete_article'),
]