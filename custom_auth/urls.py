from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import apis


urlpatterns = [
    path('login/', apis.login_view, name='login'),
    path('logout/', apis.logout_view, name='logout'),
    path('check-session/', apis.check_session, name='check_session'),
    path('check-groups/', apis.check_groups, name='check_groups'),
    path('password-reset/', apis.password_reset, name='password_reset'),
    path('new-account-user/', apis.new_account_user, name='new_account_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
]
