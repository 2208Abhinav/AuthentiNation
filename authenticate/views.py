from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from .custom_authenticators import UpdateUserProfile, RegisterUser
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request, 'authenticate/home.html', {})


def login_user(request):
    # Here we are creating login page.
    if request.method == 'POST':
        # This part registers and login the user
        username = request.POST['username']
        password = request.POST['password']
        # This is where we are creating user object 😉
        user = authenticate(request, username=username, password=password)
        # This checks if the user exists by checking in the database.
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have Been Logged In!!')
            return redirect('home')
        else:
            messages.error(request, 'Error While Logging In - '
                                    'Please check your credentials')
            return redirect('login')

    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You Have Logged Out...')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form_data = request.POST
        new_user = RegisterUser(form_data)
        if new_user.is_valid():
            new_user.save()
            username = new_user.cleaned_data['username']
            password = new_user.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'You have registered successfully'
                                      ' and logged in!!')
            return redirect('home')
        else:
            messages.error(request, "You have errors in you form...")
            return render(request, 'authenticate/register.html', {'username': form_data.get('username'),
                                                                  'first_name': form_data.get('first_name'),
                                                                  'last_name': form_data.get('last_name'),
                                                                  'email': form_data.get('email')})
    else:
        return render(request, 'authenticate/register.html', {})


def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form_data = request.POST
        existing_user = UpdateUserProfile(form_data, instance=current_user)
        if existing_user.is_valid():
            existing_user.save()
            messages.success(request, "Your user profile is updated...")
            return redirect('home')
        else:
            messages.error(request, "You have errors in you form...")
            return render(request, 'authenticate/edit_profile.html', {'username': current_user.username,
                                                                      'first_name': current_user.first_name,
                                                                      'last_name': current_user.last_name,
                                                                      'email': current_user.email})

    else:                                                  # UserChangeForm requires current "password" in form.
        return render(request, 'authenticate/edit_profile.html', {'username': current_user.username,
                                                                  'first_name': current_user.first_name,
                                                                  'last_name': current_user.last_name,
                                                                  'email': current_user.email})


def change_password(request):
    if request.method == 'POST':
        current_user = request.user
        form_data = request.POST
        changed_password = PasswordChangeForm(data=form_data, instance=current_user)
        if changed_password.is_valid():
            changed_password.save()
            messages.success(request, "Your Password Changed Successfully...")
            return redirect('home')
        else:
            messages.error(request, "You have errors in you form...")
            return render(request, 'authenticate/change_password.html', {})

    else:
        return render(request, 'authenticate/change_password.html', {})
