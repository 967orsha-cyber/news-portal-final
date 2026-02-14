from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .emails import send_welcome_email
from .emails import send_new_post_notification
from .models import Post

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group = Group.objects.get(name='common')
        instance.groups.add(common_group)

def send_welcome_email_signal(sender, instance, created, **kwargs):
    if created and instance.email:
        send_welcome_email(instance)

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:  # только при создании новой статьи
        send_new_post_notification(instance)