from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_welcome_email(user):
    subject = 'Добро пожаловать на наш новостной портал!'
    message = f'''
    Здравствуйте, {user.username}!
    
    Вы успешно зарегистрировались на нашем портале.
    
    Теперь вы можете:
    - Читать новости и статьи
    - Подписываться на категории
    - Получать еженедельные рассылки
    
    С уважением,
    команда портала
    '''
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def send_new_post_notification(post):
    subject = f'Новая статья в категории: {post.category.name}'
    
    for subscriber in post.category.subscribers.all():
        message = f'''
        Здравствуйте, {subscriber.username}!
        
        В категории "{post.category.name}" появилась новая статья:
        
        {post.title}
        
        Краткое содержание:
        {post.content[:200]}...
        
        Ссылка на статью: 
        http://127.0.0.1:8000{reverse('news_detail', args=[post.id])}
        
        С уважением,
        команда портала
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [subscriber.email],
            fail_silently=False,
        )