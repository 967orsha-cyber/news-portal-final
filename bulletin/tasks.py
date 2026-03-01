from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@shared_task
def send_response_notification(response_id):
    """
    Уведомление автору объявления о новом отклике
    """
    from .models import Response
    
    try:
        response = Response.objects.select_related('bulletin__author', 'author').get(id=response_id)
        bulletin_author = response.bulletin.author
        
        html_content = render_to_string('email/response_notification.html', {
            'response': response,
            'bulletin': response.bulletin,
            'author': response.author,
            'site_url': settings.SITE_URL
        })
        
        msg = EmailMultiAlternatives(
            subject=f'Новый отклик на объявление "{response.bulletin.title}"',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[bulletin_author.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        logger.info(f"Response notification sent to {bulletin_author.email}")
        
    except Exception as e:
        logger.error(f"Failed to send response notification: {e}")
        raise e


@shared_task
def send_response_accepted_notification(response_id):
    """
    Уведомление автору отклика о том, что его отклик принят
    """
    from .models import Response
    
    try:
        response = Response.objects.select_related('bulletin', 'author').get(id=response_id)
        
        html_content = render_to_string('email/response_accepted.html', {
            'response': response,
            'bulletin': response.bulletin,
            'site_url': settings.SITE_URL
        })
        
        msg = EmailMultiAlternatives(
            subject=f'Ваш отклик принят!',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[response.author.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        logger.info(f"Response accepted notification sent to {response.author.email}")
        
    except Exception as e:
        logger.error(f"Failed to send response accepted notification: {e}")
        raise e