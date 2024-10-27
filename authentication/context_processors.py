from .models import UserProfile
import logging
logger = logging.getLogger(__name__)

def user_role(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            role = profile.role
            logger.debug(f"Current user: {request.user.username}, Role: {role}")
        except UserProfile.DoesNotExist:
            role = None
            logger.debug(f"UserProfile does not exist for user: {request.user.username}")
    else:
        role = None
    print("role skarang", role)
    return {'user_role': role}

def user_name(request):
    if request.user.is_authenticated:
        name = request.user.get_full_name() or request.user.username
    else:
        name = None
    return {'user_name': name}