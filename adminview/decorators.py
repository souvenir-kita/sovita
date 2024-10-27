from django.http import HttpResponseForbidden
from authentication.models import UserProfile

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in.")
        
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if not user_profile or user_profile.role != 'admin':
            return HttpResponseForbidden("You do not have permission to access this page.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view