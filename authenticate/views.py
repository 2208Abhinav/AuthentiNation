from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .custom_authenticators import UpdateUserProfileForm, RegisterUserForm
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request, 'authenticate/home.html', {})


class LoginUser(View):
    # Here we are creating login page.
    def get(self, request):
        return render(request, 'authenticate/login.html', {})

    def post(self, request):
        if request.method == 'POST':
            # This part registers and login the user
            username = request.POST['username']
            password = request.POST['password']
            # This is where we are creating user object 😉
            user = authenticate(request, username=username, password=password)
            # This checks if the user exists by checking in the database.
            if user is not None:
                login(request, user)
                # Add the following code to set the time for which the
                # user should be kept logged in.
                # If the value is 0 the user session will expire when the
                # user will close the browser.
                """  request.session.set_expiry(time) """
                messages.success(request, 'You Have Been Logged In!!')
                return redirect('home')
            else:
                messages.error(request, 'Error While Logging In - '
                                        'Please check your credentials')
                return redirect('login')


class LogoutUser(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You Have Logged Out...')
        return redirect('home')


class RegisterUser(View):
    def get(self, request):
        return render(request, 'authenticate/register.html', {})

    def post(self, request):
        form_data = request.POST
        new_user = RegisterUserForm(form_data)
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


class EditUserProfile(View):
    def get(self, request):
        current_user = request.user
        return render(request, 'authenticate/edit_profile.html', {'username': current_user.username,
                                                                  'first_name': current_user.first_name,
                                                                  'last_name': current_user.last_name,
                                                                  'email': current_user.email})

    def post(self, request):
        current_user = request.user
        form_data = request.POST
        existing_user = UpdateUserProfileForm(form_data, instance=current_user)
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


class ChangePassword(View):
    def get(self, request):
        return render(request, 'authenticate/change_password.html', {})

    def post(self, request):
        current_user = request.user
        form_data = request.POST
        changed_password_profile = PasswordChangeForm(data=form_data, user=current_user)
        if changed_password_profile.is_valid():
            changed_password_profile.save()
            # This keeps the user logged in by updating the session hash.
            update_session_auth_hash(request, changed_password_profile.user)
            messages.success(request, "Your Password Changed Successfully...")
            # messages.success(request, "Please login again.")
            return redirect('home')
        else:
            messages.error(request, "You have errors in you form...")
            return render(request, 'authenticate/change_password.html', {})
