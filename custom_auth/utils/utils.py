from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives



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