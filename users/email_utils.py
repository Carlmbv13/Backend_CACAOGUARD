from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import uuid

def send_verification_email(user, request):
    """Send email verification link to user"""
    if not user.profile.email_verification_token:
        user.profile.email_verification_token = uuid.uuid4()
    
    user.profile.verification_sent_at = timezone.now()
    user.profile.save()
    
    verification_url = f"{settings.FRONTEND_URL}/verify-email/{user.profile.email_verification_token}"
    
    subject = 'Verify Your Email - CacaoGuard'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
            <div style="text-align: center; background-color: #2e7d32; padding: 20px; border-radius: 10px;">
                <h1 style="color: white;">🌱 CacaoGuard</h1>
            </div>
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-top: 10px;">
                <h2>Welcome to CacaoGuard, {user.username}!</h2>
                <p>Please verify your email address to activate your account.</p>
                <p style="text-align: center;">
                    <a href="{verification_url}" style="display: inline-block; padding: 12px 24px; background-color: #2e7d32; color: white; text-decoration: none; border-radius: 5px;">
                        Verify Email Address
                    </a>
                </p>
                <p>Or copy this link to your browser:</p>
                <p style="color: #666; font-size: 12px;">{verification_url}</p>
                <hr>
                <p style="color: #666; font-size: 12px;">This link will expire in 24 hours.</p>
                <p style="color: #666; font-size: 12px;">If you didn't create an account with CacaoGuard, please ignore this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
    Welcome to CacaoGuard, {user.username}!
    
    Please verify your email address by clicking the link below:
    
    {verification_url}
    
    This link will expire in 24 hours.
    
    If you didn't create an account with CacaoGuard, please ignore this email.
    """
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
            html_message=html_message
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False


def is_verification_token_valid(profile):
    """Check if verification token is still valid (24 hours)"""
    if not profile.verification_sent_at:
        return False
    
    expiry_time = profile.verification_sent_at + timedelta(hours=24)
    return timezone.now() < expiry_time