from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from .models import Post
from .filters import PostFilter
from .forms import NewsForm 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Category
from django.core.cache import cache

class CacheDetailMixin:
    """
    Миксин для кеширования детальной страницы объекта
    Использование: class NewsDetail(CacheDetailMixin, DetailView):
    """
    cache_timeout = 60 * 15  # 15 минут по умолчанию
    
    def get_object(self, queryset=None):
        # Формируем ключ кеша: модель_класс_первичныйключ
        obj_id = self.kwargs.get('pk')
        cache_key = f"{self.model.__name__.lower()}_detail_{obj_id}"
        
        # Пробуем получить из кеша
        obj = cache.get(cache_key)
        
        if not obj:
            # Если нет в кеше — грузим из БД
            obj = super().get_object(queryset)
            cache.set(cache_key, obj, self.cache_timeout)
            self.from_cache = False
            print(f"{self.model.__name__} {obj_id} загружен из БД и закеширован")
        else:
            self.from_cache = True
            print(f"{self.model.__name__} {obj_id} загружен из КЕША")
        
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['from_cache'] = getattr(self, 'from_cache', False)
        return context
 

class NewsUpdate(UpdateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/news_create.html'  
    success_url = reverse_lazy('news_list')
    
    def form_valid(self, form):
        form.instance.post_type = 'NW'  
        return super().form_valid(form)
    
class ArticleUpdate(UpdateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/article_create.html'  
    success_url = reverse_lazy('articles_list')
    
    def form_valid(self, form):
        form.instance.post_type = 'AR'  
        return super().form_valid(form)
    
class NewsDelete(CacheDetailMixin, DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')
    context_object_name = 'news'
    # Если нужно своё время кеша:
    # cache_timeout = 60 * 30  # 30 минут
    
    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS)
    
class ArticleDelete(CacheDetailMixin, DeleteView):
    model = Post
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('articles_list')
    context_object_name = 'article'
    
    def get_queryset(self):
        return Post.objects.filter(post_type=Post.ARTICLE)

class NewsCreate(CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('news_list')
    
    def form_valid(self, form):
        form.instance.post_type = 'NW'
        # ВРЕМЕННО: берём первого автора
        from .models import Author
        form.instance.author = Author.objects.first()
        return super().form_valid(form)
    
class ArticleCreate(CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/article_create.html'
    success_url = reverse_lazy('articles_list')
    
    def form_valid(self, form):
        form.instance.post_type = 'AR'
        # ВРЕМЕННО: берём первого автора
        from .models import Author
        form.instance.author = Author.objects.first()
        return super().form_valid(form)

class NewsSearch(FilterView):
    model = Post
    template_name = 'news/news_search.html'
    context_object_name = 'news_list'
    filterset_class = PostFilter
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS).order_by('-created_at')

class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS).order_by('-created_at')
    
class ArticleList(ListView):
    model = Post
    template_name = 'news/article_list.html'
    context_object_name = 'articles_list'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(post_type=Post.ARTICLE).order_by('-created_at')

class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

class ArticleDetail(DetailView):
    model = Post
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/post_form.html'
    permission_required = 'news.add_post'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_type = 'news'
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/post_form.html'
    permission_required = 'news.change_post'
    
    def form_valid(self, form):
        form.instance.post_type = 'news'
        return super().form_valid(form)

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/post_form.html'
    permission_required = 'news.add_post'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_type = 'article'
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/post_form.html'
    permission_required = 'news.change_post'
    
    def form_valid(self, form):
        form.instance.post_type = 'article'
        return super().form_valid(form)
    
class BecomeAuthor(LoginRequiredMixin, View):
    def get(self, request):
        authors_group = Group.objects.get(name='authors')
        request.user.groups.add(authors_group)
        return redirect('news_list')
    
class SubscribeToCategoryView(LoginRequiredMixin, View):
    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        request.user.subscribed_categories.add(category)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class UnsubscribeFromCategoryView(LoginRequiredMixin, View):
    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        request.user.subscribed_categories.remove(category)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
