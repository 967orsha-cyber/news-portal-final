from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .models import Post
from .tasks import send_welcome_email_task, send_new_post_notification_task

User = get_user_model()

@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    if created:
        send_welcome_email_task.delay(instance.id)


@receiver(post_save, sender=Post)
def post_created_handler(sender, instance, created, **kwargs):
    if created:
        send_new_post_notification_task.delay(instance.id)


@receiver(post_save, sender=Post)
def clear_post_cache_on_update(sender, instance, **kwargs):
    """Очищает кеш статьи при любом сохранении (создание или обновление)"""
    cache_key = f"post_detail_{instance.id}"
    cache.delete(cache_key)