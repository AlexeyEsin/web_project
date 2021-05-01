from django.contrib import admin
from django.urls import path, re_path, include
from authorization import views as CustomAuthViews
from django.contrib.auth import views as AuthViews
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('articles/', include('articles.urls')),
    path('login/', AuthViews.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('sign-up/', CustomAuthViews.sign_up, name='sign-up'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
