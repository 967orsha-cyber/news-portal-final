from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Post

class Command(BaseCommand):
    help = 'Create groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Создаём группы
        common_group, _ = Group.objects.get_or_create(name='common')
        authors_group, _ = Group.objects.get_or_create(name='authors')
        
        # Получаем права для модели Post
        content_type = ContentType.objects.get_for_model(Post)
        permissions = Permission.objects.filter(content_type=content_type)
        
        # Даём авторам все права на Post
        authors_group.permissions.set(permissions)
        
        self.stdout.write(self.style.SUCCESS('Groups created successfully!'))