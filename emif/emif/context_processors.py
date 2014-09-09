from django.conf import settings

from accounts.models import EmifProfile, Profile

def debug(context):
  return {'DEBUG': settings.DEBUG}

def baseurl(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'
        
    return {'BASE_URL': scheme + request.get_host() + settings.BASE_URL,}

# make user personal profiles available everywhere
def profiles_processor(request):
    profiles = []

    if request.user.is_authenticated():
        try:
        
            user_profile = EmifProfile.objects.get(user = request.user)

            profiles = user_profile.profiles.all()
        
        except EmifProfile.DoesNotExist:
            pass

    return { 'profiles': profiles }