from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
import json

from .serializers import UserSerializer


# Create your views here.


@csrf_exempt
@api_view(['POST'])
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
    print(request.user.username)
    return JsonResponse({'authenticated': True, "user": request.user.username})