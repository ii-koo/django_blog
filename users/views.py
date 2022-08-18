from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForms, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForms(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('blog-home')
    else:
        form = UserRegistrationForms()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        userForm = UserUpdateForm(request.POST, instance=request.user)
        profileForm = ProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, f'Your account has been updated')
            return redirect('blog-profile')
    else:
        userForm = UserUpdateForm(instance=request.user)
        profileForm = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'userform': userForm,
            'profileform': profileForm
        }
        return render(request, 'profile.html', context)
