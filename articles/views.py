from django.shortcuts import render, redirect, reverse
from .models import Section, Article
from .forms import ArticleForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group

def articles_view(request, section, article_id):
    if not request.user.is_authenticated:
        return redirect('home')

    sections = Section.objects.all()
    try:
        selected_section = Section.objects.get(name=section)
    except Section.DoesNotExist:
        error_status = '404'
        error_message = 'Страница не найдена'
        error_description = 'Такой страницы не существует.'
        params = {'sections': sections, 'error_status': error_status, 'error_message': error_message, 'error_description': error_description }
        return render(request, 'main/error.html', params)

    if article_id == 0:
        if selected_section.article_set.exists():
            selected_article = selected_section.article_set.first()
            return redirect('article_view', section, selected_article.id)
        else:
            return render(request, 'articles/article_view.html', {'sections': sections, 'selected_section': selected_section})

    elif selected_section.article_set.filter(id=article_id).exists():
        selected_article = selected_section.article_set.get(id=article_id)
    else:
        error_status = '404'
        error_message = 'Страница не найдена'
        error_description = 'Такой страницы не существует.'
        params = {'sections': sections, 'error_status': error_status, 'error_message': error_message, 'error_description': error_description }
        return render(request, 'main/error.html', params)
    
    params = {'selected_section': selected_section, 'sections': sections, 'selected_article': selected_article}
    return render(request, 'articles/article_view.html', params)


def create_article_view(request):
    if not request.user.is_authenticated:
        return redirect('home')

    sections = Section.objects.all()
    if request.user.groups.filter(name = 'Редактор').exists() or request.user.is_superuser:
        error = ''
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            if form.is_valid():
                form.save()
                section = form.cleaned_data['section']
                return redirect('article_view', section, 0)
            else:
                error = 'Некоррекнтые данные'

        form = ArticleForm()

        params = {'sections': sections, 'form': form, 'error': error}
        return render(request, 'articles/create_article.html', params)
    else:
        error_status = '403'
        error_message = 'Доступ ограничен'
        error_description = 'У вас недостаточно прав для просмотра этой страницы.'
        params = {'sections': sections, 'error_status': error_status, 'error_message': error_message, 'error_description': error_description }
        return render(request, 'main/error.html', params)


def update_article_view(request, section, article_id):
    if not request.user.is_authenticated:
        return redirect('home')

    sections = Section.objects.all()
    if request.user.groups.filter(name = 'Редактор').exists() or request.user.is_superuser:
        error = ''
        if request.method == 'POST':
            article = Article.objects.get(id=article_id)
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                section = form.cleaned_data['section']
                return redirect('article_view', section, article_id)
            else:
                error = 'Некоррекнтые данные'

        article = Article.objects.get(id=article_id)
        form = ArticleForm(instance=article)

        params = {'sections': sections, 'form': form, 'error': error, 'section': section, 'article_id': article_id}
        return render(request, 'articles/update_article.html', params)
    else:
        error_status = '403'
        error_message = 'Доступ ограничен'
        error_description = 'У вас недостаточно прав для просмотра этой страницы.'
        params = {'sections': sections, 'error_status': error_status, 'error_message': error_message, 'error_description': error_description }
        return render(request, 'main/error.html', params)


def delete_article_view(request, section, article_id):
    if not request.user.is_authenticated:
        return redirect('home')

    sections = Section.objects.all()
    if request.user.groups.filter(name = 'Редактор').exists() or request.user.is_superuser:
        error = ''
        if request.method == 'POST':
            article = Article.objects.get(id=article_id)
            article.delete()
            return redirect('article_view', section, 0)

        article_name = Article.objects.get(id=article_id).header
        params = {'sections': sections, 'section': section, 'article_id': article_id, 'article_name': article_name}
        return render(request, 'articles/delete_article.html', params)
    else:
        error_status = '403'
        error_message = 'Доступ ограничен'
        error_description = 'У вас недостаточно прав для просмотра этой страницы.'
        params = {'sections': sections, 'error_status': error_status, 'error_message': error_message, 'error_description': error_description }
        return render(request, 'main/error.html', params)

