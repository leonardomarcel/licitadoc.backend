from django.urls import path

from . import apis


urlpatterns = [
    path('api/login/', apis.login_view, name='login'),
    path('api/logout/', apis.logout_view, name='logout'),
    path('api/check-session/', apis.check_session, name='check_session'),
    path('api/check-groups/', apis.check_groups, name='check_groups'),

    
]
