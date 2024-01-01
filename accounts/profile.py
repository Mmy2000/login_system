from .models import Profile

def myprofile(request):
    profile = Profile.objects.get(user=request.user)

    return dict(profile=profile)