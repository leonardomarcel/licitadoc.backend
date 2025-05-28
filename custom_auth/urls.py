from django.urls import path

from . import apis


urlpatterns = [
    path('login/', apis.login_view, name='login'),
    path('logout/', apis.logout_view, name='logout'),
    path('check-session/', apis.check_session, name='check_session'),
    path('check-groups/', apis.check_groups, name='check_groups'),
    path('password-reset/', apis.password_reset, name='password_reset'),
    path('new-account-user/', apis.new_account_user, name='new_account_user'),

    
]
