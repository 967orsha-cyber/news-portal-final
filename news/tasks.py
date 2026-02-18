from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email_task(user_id):
    """
    Асинхронная отправка приветственного письма
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        user = User.objects.get(id=user_id)
        
        html_content = render_to_string('email/welcome_email.html', {
            'user': user,
            'site_url': settings.SITE_URL
        })
        
        msg = EmailMultiAlternatives(
            subject='Добро пожаловать на NewsPortal!',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        logger.info(f"Welcome email sent to {user.email}")
        return f"Welcome email sent to {user.email}"
    
    except Exception as e:
        logger.error(f"Failed to send welcome email: {e}")
        raise e


@shared_task
def send_new_post_notification_task(post_id):
    """
    Асинхронная отправка уведомлений подписчикам категории
    """
    from news.models import Post
    
    try:
        post = Post.objects.get(id=post_id)
        
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
            
            logger.info(f"Notifications sent for post {post_id} in category {category.name}")
        
        return f"Notifications sent for post {post_id}"
    
    except Exception as e:
        logger.error(f"Failed to send post notifications: {e}")
        raise e


@shared_task
def send_weekly_newsletter_task():
    """
    Асинхронная еженедельная рассылка
    """
    from django.contrib.auth import get_user_model
    from news.models import Category
    User = get_user_model()
    
    week_ago = timezone.now() - timedelta(days=7)
    sent_count = 0
    
    try:
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
                sent_count += 1
        
        logger.info(f"Weekly newsletter sent to {sent_count} users")
        return f"Weekly newsletter sent to {sent_count} users"
    
    except Exception as e:
        logger.error(f"Failed to send weekly newsletter: {e}")
        raise e