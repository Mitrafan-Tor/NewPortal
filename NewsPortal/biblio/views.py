from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from datetime import datetime
from .search import SearchPost
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages



#Новости
class NewsList(PermissionRequiredMixin, ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(post_type='NW').order_by('-created_at')
    paginate_by = 10
    permission_required = ('biblio.view_post',)

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset().filter(post_type='NW')
        self.filterset = SearchPost(self.request.GET, queryset)
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        # Добавляем подсчет новостей и статей
        context['news_count'] = Post.objects.filter(post_type='NW').count()
        context['article_count'] = Post.objects.filter(post_type='AR').count()
        context['time_now'] = datetime.now()
        context['next_sale'] = "Распродажа в среду!"
        return context

class NewsDetail(PermissionRequiredMixin, DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    permission_required = ('biblio.view_post',)


# Добавляем новое представление для создания товаров.
class PostCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news/news_create.html'
    permission_required = ('biblio.add_post',)

    def get_success_url(self):
        return reverse('biblio:news_detail', kwargs={'pk': self.object.pk})





class PostEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news/news_edit.html'
    permission_required = ('biblio.change_post',)


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list'),
    permission_required = ('biblio.delete_post',)


#СТАТЬИ
class ArticlesList(PermissionRequiredMixin, ListView):
    model = Post
    template_name = 'articles/articles_list.html'
    context_object_name = 'article'
    queryset = Post.objects.filter(post_type='AR').order_by('-created_at')
    paginate_by = 10
    permission_required = ('biblio.view_post',)

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset().filter(post_type='AR')
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = SearchPost(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        # Добавляем подсчет новостей и статей
        context['news_count'] = Post.objects.filter(post_type='NW').count()
        context['article_count'] = Post.objects.filter(post_type='AR').count()
        context['time_now'] = datetime.now()
        context['next_sale'] = "Распродажа в среду!"
        return context

class ArticlesDetail(PermissionRequiredMixin, DetailView):
     model = Post
     template_name = 'articles/articles_detail.html'
     context_object_name = 'article'
     permission_required = ('biblio.view_post',)


# # Добавляем новое представление для создания товаров.
class ArticlesCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'articles/articles_create.html'
    permission_required = ('biblio.add_post',)

 # Добавляем представление для изменения товара.
class ArticlesEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'articles/articles_edit.html'
    permission_required = ('biblio.change_post',)

# Представление удаляющее товар.
class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'articles/articles_delete.html'
    success_url = reverse_lazy('articles_list')
    permission_required = ('biblio.delete_post',)


class CategoryListView(NewsList):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'
    filterset = None  # Явно отключаем фильтрацию

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = super().get_queryset().filter(categories=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем информацию о подписке, если есть подписчики
        if hasattr(self.category, 'subscribers'):
            context['is_not_subscriber'] = (
                    self.request.user.is_authenticated and
                    self.request.user not in self.category.subscribers.all()
            )

        context['category'] = self.category
        return context

@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    messages.success(request, f'Вы подписались на категорию "{category.name}"')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def unsubscribe_from_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.remove(request.user)
    messages.success(request, f'Вы отписались от категории "{category.name}"')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

