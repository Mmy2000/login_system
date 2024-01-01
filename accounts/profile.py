from .models import Profile

def myprofile(request):
    current_user = request.user
    profile = None
    if  current_user.is_authenticated:
        profile = Profile.objects.get(user=current_user)

    return dict(profile=profile)