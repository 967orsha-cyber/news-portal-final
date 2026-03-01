from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

User = get_user_model()

class Category(models.Model):
    """Категории объявлений (Танки, Хилы, ДД и т.д.)"""
    TANKS = 'TK'
    HEALERS = 'HL'
    DD = 'DD'
    TRADERS = 'TR'
    GUILDMASTERS = 'GM'
    QUESTGIVERS = 'QG'
    BLACKSMITHS = 'BS'
    LEATHERWORKERS = 'LW'
    POTIONMAKERS = 'PM'
    SPELLMASTERS = 'SM'
    
    CATEGORY_CHOICES = [
        (TANKS, 'Танки'),
        (HEALERS, 'Хилы'),
        (DD, 'ДД'),
        (TRADERS, 'Торговцы'),
        (GUILDMASTERS, 'Гилдмастеры'),
        (QUESTGIVERS, 'Квестгиверы'),
        (BLACKSMITHS, 'Кузнецы'),
        (LEATHERWORKERS, 'Кожевники'),
        (POTIONMAKERS, 'Зельевары'),
        (SPELLMASTERS, 'Мастера заклинаний'),
    ]
    
    name = models.CharField(max_length=2, choices=CATEGORY_CHOICES, unique=True)
    
    def __str__(self):
        return dict(self.CATEGORY_CHOICES)[self.name]
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Bulletin(models.Model):
    """Объявление"""
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = RichTextField(verbose_name='Содержание')  # WYSIWYG-поле
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='bulletins', verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bulletins', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

class Response(models.Model):
    """Отклик на объявление"""
    text = models.TextField(verbose_name='Текст отклика')
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE, related_name='responses', verbose_name='Объявление')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    accepted = models.BooleanField(default=False, verbose_name='Принят')
    
    def __str__(self):
        return f'Отклик от {self.author.username} на {self.bulletin.title}'
    
    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-created_at']
