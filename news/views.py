from django.views.generic import ListView, DetailView
from .models import Post

class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS).order_by('-created_at')

class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
