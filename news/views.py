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
    
class NewsDelete(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')
    
    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS)
    
class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('articles_list')
    
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
