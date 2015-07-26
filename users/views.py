import datetime
import hashlib
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from .forms import RegistrationForm, LoginForm, ConfirmationForm
from .models import UserProfile


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random()).encode()).hexdigest()[:5]
            activation_key = hashlib.sha1((salt+email).encode()).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            user = User.objects.get(username=username)

            new_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()
            full_url = request.build_absolute_uri(
                reverse('confirm', kwargs={'activation_key': activation_key})
            )
            email_subject = 'Rejestracja konta'
            email_body = 'By aktywować konto kliknij w poniższy link\n%s' \
                         % full_url
            send_mail(email_subject, email_body, settings.EMAIL_ADMIN, [email],
                      fail_silently=False)
            messages.add_message(request, messages.SUCCESS,
                                 'Email z potwierdzeniem został wysłany')
            return redirect(reverse('register'))
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_confirm(request, activation_key):
    if request.user.is_authenticated():
        return redirect(reverse('home-page'))
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    if user_profile.key_expires < timezone.now():
        return render(request, 'confirm_expired.html',
                      {'form': ConfirmationForm})

    user = user_profile.user
    if user.is_active:
        messages.add_message(request, messages.WARNING, 'Błędne żądanie')
        return redirect(reverse('home-page'))
    user.is_active = True
    user.save()
    messages.add_message(request, messages.SUCCESS, 'Możesz się zalogować')
    return redirect(reverse('login'))


def resend_confirmation(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = get_object_or_404(User, email=email)
        if user.is_active:
            messages.add_message(request, messages.WARNING, 'Błędne żądanie')
            return redirect(reverse('home-page'))
        user_profile = UserProfile.objects.get(user=user)
        salt = hashlib.sha1(str(random.random()).encode()).hexdigest()[:5]
        activation_key = hashlib.sha1((salt+email).encode()).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        user_profile.activation_key = activation_key
        user_profile.key_expires = key_expires
        user_profile.save()
        full_url = request.build_absolute_uri(
            reverse('confirm', kwargs={'activation_key': activation_key})
        )
        email_subject = 'Rejestracja konta'
        email_body = 'By aktywować konto kliknij w poniższy link\n%s' \
                     % full_url
        send_mail(email_subject, email_body, settings.EMAIL_ADMIN, [email],
                  fail_silently=False)
        messages.add_message(request, messages.SUCCESS,
                             'Email z potwierdzeniem został wysłany')
        return redirect(reverse('register'))


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('logout'))


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('home-page'))
                else:
                    messages.add_message(request, messages.WARNING,
                                         'Potwierdź najpierw konto')
            else:
                messages.add_message(request, messages.DANGER,
                                     'Zły login lub hasło')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})