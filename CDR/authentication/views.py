from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import generate_token
import logging
log = logging.getLogger(__name__)


import sys
sys.path.append("..")
# Create your views here.
from CDR import settings


def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists!")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered!")
            return redirect('home')

        if len(username) > 50:
            messages.error(request, "Username cannot be more than 50 characters long!")

        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")

        if not username.isalnum():
            messages.error(request, "Username must be alpha-numeric!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        # myuser.save()

        messages.success(request, "Your account has been created successfully! Please click on the confirmation link "
                                  "sent to your email address to activate your account.")

        # welcome email
        subject = "Welcome to CDR!"
        message = "Hello " + myuser.first_name + "!!\n\n\nWelcome to CDR!\n\nThank you for visiting our website.\nWe " \
                                                 "have " \
                                                 "also sent you a confirmation email. Please confirm your email " \
                                                 "address in order to activate your account and continue using " \
                                                 "CDR.\n\nThanking You,\nGAMP "

        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ CDR"
        message2 = render_to_string('email_confirmation.html', {

            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "authentication/signup.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        log.debug("0000000000")
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        log.debug("111111111")
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})
        else:
            messages.error(request, "bad credentials!")
            return redirect('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')
