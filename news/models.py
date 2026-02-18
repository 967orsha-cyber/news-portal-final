from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    
    def update_rating(self):
        # Рейтинг статей автора × 3
        post_rating = sum(post.rating for post in self.post_set.all()) * 3
        
        # Рейтинг всех комментариев автора
        comment_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        
        # Рейтинг всех комментариев к статьям автора
        author_post_ids = self.post_set.values_list('id', flat=True)
        comments_to_author_posts = Comment.objects.filter(post__id__in=author_post_ids)
        comments_to_posts_rating = sum(comment.rating for comment in comments_to_author_posts)
        
        # Общий рейтинг
        self.rating = post_rating + comment_rating + comments_to_posts_rating
        self.save()
    
    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(
        User, 
        related_name='subscribed_categories',
        blank=True
    )
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    
    categories = models.ManyToManyField(Category, through='PostCategory')
    
    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])
    
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.post.title} - {self.category.name}'
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
    
    def __str__(self):
        return f'{self.user.username} - {self.text[:50]}'
