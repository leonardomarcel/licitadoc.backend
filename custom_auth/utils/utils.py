from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from custom_auth.models import CustomUser as User



def send_email(subject, message, from_email, to_email, html_message=None):
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=from_email,
        to=[to_email],
    )
    if html_message:
        email.attach_alternative(html_message, "text/html")
    email.send()

def generate_password():
    import secrets
    import string

    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for i in range(12))
    return password

def check_valid_email(email):
    import re
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    used_emails = User.objects.values_list('email', flat=True)
    if re.fullmatch(regex, email) and email not in used_emails:
        return {'valid': True, 'reason': None}
    else:
        return {'valid': False, 'reason': 'Email inválido'}
    