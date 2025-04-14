from django.http import JsonResponse
from functools import wraps

def require_group(*group_names):

    """
    Decorator for views that checks whether the current user has a group
    matching one of the passed names.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({'error': 'You do not have permission to access this resource.'}, status=403)
        return _wrapped_view
    return decorator
    