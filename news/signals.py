from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Post
from .tasks import send_welcome_email_task, send_new_post_notification_task

User = get_user_model()

@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    """При создании пользователя отправляем приветственное письмо асинхронно"""
    if created:
        send_welcome_email_task.delay(instance.id)


@receiver(post_save, sender=Post)
def post_created_handler(sender, instance, created, **kwargs):
    """При создании поста отправляем уведомления подписчикам асинхронно"""
    if created:
        send_new_post_notification_task.delay(instance.id)