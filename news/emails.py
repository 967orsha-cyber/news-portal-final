from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

def send_welcome_email(user):
    """Приветственное письмо с HTML"""
    html_content = render_to_string('email/welcome_email.html', {
        'user': user,
        'site_url': settings.SITE_URL
    })
    
    msg = EmailMultiAlternatives(
        subject='Добро пожаловать на NewsPortal!',
        body='',  # пустой текст, только HTML
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_new_post_notification(post):
    """Уведомление подписчикам категории"""
    for category in post.categories.all():
        subscribers = category.subscribers.all()
        
        for user in subscribers:
            html_content = render_to_string('email/new_post_notification.html', {
                'post': post,
                'category': category,
                'user': user,
                'site_url': settings.SITE_URL
            })
            
            msg = EmailMultiAlternatives(
                subject=f'Новая статья в категории {category.name}',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

def send_weekly_newsletter():
    """Еженедельная рассылка"""
    from django.utils import timezone
    from datetime import timedelta
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    week_ago = timezone.now() - timedelta(days=7)
    
    for user in User.objects.filter(is_active=True):
        # Собираем новые посты из категорий, на которые подписан пользователь
        subscribed_categories = user.subscribed_categories.all()
        categories_with_posts = {}
        
        for category in subscribed_categories:
            new_posts = category.posts.filter(created_at__gte=week_ago)
            if new_posts.exists():
                categories_with_posts[category] = new_posts
        
        if categories_with_posts:
            html_content = render_to_string('email/weekly_newsletter.html', {
                'user': user,
                'categories_with_posts': categories_with_posts,
                'site_url': settings.SITE_URL
            })
            
            msg = EmailMultiAlternatives(
                subject='Еженедельная рассылка NewsPortal',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()