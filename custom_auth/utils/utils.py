from django.core.mail import send_mail


def send_email(subject, message, from_email, to_email, html_message):
    send_mail(subject, message, from_email, [to_email], html_message) 

def generate_password():
    import secrets
    import string

    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for i in range(12))
    return password