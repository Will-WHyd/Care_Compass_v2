from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import HttpResponseRedirect
from .forms import ProfileForm
from .models import Profile
from med_appt.models import Consultant
from django.contrib.auth.models import User
from itertools import chain


# Create your views here.
def profile_view(request):
    """
    Renders the most recent information on the user's profile page.
    Displays an individual instance of :model: 'user_profile.Profile'

    Additionally, creates list of consultants to display on profile page

    **Context**
    ``profile`` 
        An instance of :model:`user_profile.Profile`
    """
    profile = get_object_or_404(Profile, user=request.user)

    if request.user.is_authenticated:
        # Collects both public consultants and profile-associated private consultants
        try:
            public_consultants = Consultant.objects.filter(private=False)
            private_consultants = Consultant.objects.filter(private=True, clients=profile)
            consultants = list(chain(public_consultants, private_consultants))
        except Profile.DoesNotExist:
            consultants = Consultant.objects.filter(private=False)
    else:
            consultants = Consultant.objects.filter(private=False)

    return render(request, "profile/profile.html", {"profile": profile, "consultants": consultants})


@login_required
def edit_profile(request):
    """
    Renders the profile settings edit page
    **Context**
    ``profile`` 
        An instance of :model:`user_profile.Profile`
    """
    template = "edit_profile.html"
    profile = get_object_or_404(Profile, user=request.user)
    profile_form = ProfileForm()

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Profile Details Updated'
                )
            return redirect('profile:profile')
        else:
            messages.error(request, form.errors)
            return redirect('profile:profile')
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profile/edit_profile.html', {'profile_form': profile_form, 'profile': profile})


@login_required
def delete_account(request):
    """
    Deletes the user and associated data. 
    """
    user = get_object_or_404(User, id=request.user.id)

    if user.is_superuser:
        # Prevent deletion of superuser account
        messages.error(request, 'Admin accounts cannot be deleted.')
        return redirect('appointments:home')

    try:
        user.delete()
        messages.success(request, 'Your account has been deleted successfully!')
        return redirect('appointments:home')
    except Exception as e: 
        messages.error(request, 'Oops! Something went wrong!')
        return redirect('appointments:home')