from django.contrib.sites.models import Site
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

# Список всех постов
class PostList(ListView):
    model = Post  # выводим посты
    ordering = '-time_add'  # сортировка по дате создания
    template_name = 'posts.html'  # шаблон для вывода
    context_object_name = 'posts'  # имя списка, по которому будет обращение из html-шаблона
    paginate_by = 10  # количество постов на странице

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        queryset = super().get_queryset()  # получаем обычный запрос
        self.filterset = PostFilter(self.request.GET, queryset)  # сохраняем фильтрацию в объекте класса
        return self.filterset.qs  # возвращаем отфильтрованный список постов

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset  # добавляем в контекст объект фильтрации
        return context


# Подробности по каждому посту
class PostDetail(DetailView):
    model = Post  # выводим посты
    template_name = 'post.html'  # шаблон для вывода
    context_object_name = 'post'  # имя списка, по которому будет обращение из html-шаблона

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Представление для создания поста с проверкой прав
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return redirect(f'/news/{Post.objects.latest("id").id}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Представление для изменения поста с проверкой прав (форма и шаблон как для создания поста)
class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


# Представление для удаления поста
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')  # после удаления перенаправляем на страницу со списком постов


# Список постов по категориям
class CategoryPostList(ListView):
    model = Post # выводим посты
    ordering = '-time_add'  # сортировка по дате создания
    template_name = 'category_posts.html' # шаблон для вывода
    context_object_name = 'category_posts' # имя списка, по которому будет обращение из html-шаблона
    paginate_by = 10  # количество постов на странице

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        # метод get_object_or_404 используется на случай отсутствия категории с нужным id
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category).order_by('-time_add')  # фильтрация постов по категории
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


# Подписка на категорию постов
@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'You have successfully subscribed to the category'
    return render(request, 'subscribe.html', {'category': category, 'message': message})
