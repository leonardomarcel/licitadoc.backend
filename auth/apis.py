from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from django.template.loader import render_to_string
from .utils.utils import send_email, generate_password
from rest_framework.permissions import AllowAny
import json

from .serializers import UserSerializer


# Create your views here.


@csrf_exempt
@api_view(['POST'])
# @permission_classes([AllowAny])
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        serialized_user = UserSerializer(user)
        return JsonResponse({'user': serialized_user.data, 'success': True})
    else:
        return JsonResponse({'success': False}) 

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@login_required
def check_session(request):
    #logout(request)
    return JsonResponse({'authenticated': True, "user": request.user.username})

@login_required
def check_groups(request):
    list_groups = [group.name for group in request.user.groups.all()]
    return JsonResponse({'groups': list_groups})
@csrf_exempt
@api_view(['POST'])
def password_reset(request):
    email = request.data.get('email')
    try:
        User.objects.get(email=email)
        password = generate_password()
        html_content = render_to_string('emails/meu_email.html', {
        'password': password,
        'email': email
        })
        send_email('[Licita.doc] Email de redefinição de senha', message="oi", from_email="licitadoc@mail.com", to_email=email, html_message=html_content)
        # user.set_password(password)
        # user.save()
        return JsonResponse({'success': True, 'message': 'Se estiver cadastrado, o email foi enviado.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}) #Email enviado com sucesso'})

