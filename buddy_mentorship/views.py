from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect

from apps.users.models import User

from .models import BuddyRequest, Profile


def index(request):
    return render(request, "buddy_mentorship/home.html", {"active_page": "home"})


@login_required(login_url="login")
def profile(request, profile_id=""):
    if not profile_id:
        user = request.user
        profile_id = Profile.objects.get(user=user).id
    profile = Profile.objects.get(id=profile_id)
    context = {
        "can_request": can_request(request.user, profile.user),
        "profile": profile,
        "active_page": "profile"
    }
    return render(request, "buddy_mentorship/profile.html", context)


@login_required(login_url="login")
def send_request(request, uuid):
    user = request.user
    requestee = User.objects.get(uuid=uuid)
    if can_request(user, requestee):
        BuddyRequest.objects.create(
            requestor=user, requestee=requestee, message="Hi! Will you be my mentor?"
        )
        return redirect("requests")
    return HttpResponseForbidden("You cannot send this user a request")


# needs to be updated as we expand profile model
def can_request(requestor, requestee):
    requestor_profile = Profile.objects.get(user=requestor)
    requestee_profile = Profile.objects.get(user=requestee)
    # when possible, should be no pending existing requests
    existing_requests = BuddyRequest.objects.filter(requestor=requestor, requestee=requestee)

    return (
        requestor_profile.help_wanted 
        and requestee_profile.can_help
        and requestor.is_active
        and requestee.is_active
        and not existing_requests
    )
