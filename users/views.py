from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileEditForm
from .models import Profile


@login_required
def user_detail(request, username: str):
    user = get_object_or_404(User, username=username)

    return render(
        request,
        'users/user_detail.html',
        {
            'user': user,
        },
    )


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User profile has been successfully saved.')
            return redirect('user:user_detail.html')
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, '<users/edit_profile.html', {'form': form, 'profile': profile})


@login_required
def leave(request):
    if request.user.groups.filter(name='T').exists():
        raise PermissionDenied('Profesorado no puede abandonar la plataforma')

    if request.method == 'POST':
        request.user.is_active = False
        request.user.save()
        messages.success(request, 'Good bye! Hope to see you soon.')
        return redirect('index')
    return render(request, 'users/confirm_leave.html')
