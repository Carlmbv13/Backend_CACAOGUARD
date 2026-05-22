from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_verification_email_task(user_email, username, verification_url):
    subject = 'Verify Your Email - CacaoGuard'
    message = f"""
    Hello {username},
    
    Please click the link below to verify your email:
    
    {verification_url}
    
    This link will expire in 24 hours.
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
    return f"Email sent to {user_email}"