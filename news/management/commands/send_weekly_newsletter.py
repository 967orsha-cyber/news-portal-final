from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from news.models import Category, Post

class Command(BaseCommand):
    help = 'Send weekly newsletter with new posts from subscribed categories'

    def handle(self, *args, **options):
        week_ago = timezone.now() - timedelta(days=7)
        
        for category in Category.objects.all():
            new_posts = category.post_set.filter(created_at__gte=week_ago)
            
            if not new_posts.exists():
                continue
                
            for subscriber in category.subscribers.all():
                subject = f'Еженедельная рассылка: новые статьи в категории "{category.name}"'
                
                message = f'Здравствуйте, {subscriber.username}!\n\n'
                message += f'За прошедшую неделю в категории "{category.name}" появились новые статьи:\n\n'
                
                for post in new_posts:
                    post_url = f'http://127.0.0.1:8000{reverse("news_detail", args=[post.id])}'
                    message += f'• {post.title}\n'
                    message += f'  {post.content[:100]}...\n'
                    message += f'  Ссылка: {post_url}\n\n'
                
                message += 'С уважением,\nкоманда портала'
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [subscriber.email],
                    fail_silently=False,
                )
                
        self.stdout.write(self.style.SUCCESS('Weekly newsletter sent successfully'))