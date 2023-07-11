from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.core.paginator import Paginator
from django.views import generic
from .forms import ImageForm
from .models import Image
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .tokens import generate_token
from django.core.mail import EmailMessage, send_mail
import os
import re


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def upload(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
         form.save()
        return redirect('homepage')
    else:
       form = ImageForm()
    return render(request, 'upload.html', {'form': form})

def index(request):  
    if request.method == 'GET':
     img = Image.objects.all().order_by('-date')
     paginator = Paginator(img, 100)
     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)
     print('Img=', img)
     print()
     print('Paginator=', paginator)
     print()
     print('Page_Number=', page_number)
     print()
     print('Page_Obj=', page_obj)
     print()
     if 'q' in request.GET:
       q = request.GET['q']
       multiple_q = Q(Q(caption__icontains=q) | Q(date__icontains=q))
       page_obj = Image.objects.filter(multiple_q)
    else:
       img = Image.objects.all()
    return render(request, 'index.html', {'page_obj':page_obj})


def download(path):
   file_path = os.path.join(settings.MEDIA_ROOT, path)
   if os.path.exists(file_path):
      with open(file_path, 'rb') as fh:
         response = HttpResponse(fh.read(), content_type="image/photo")
         response['Content-Disposition'] = 'inline;filename=' + \
             os.path.basename(file_path)
         return response

   raise Http404

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username = username):
         messages.error(request, 'Username Already Exist!! Please try another username')
         return render(request, 'signup.html')

        elif User.objects.filter(email=email):
         messages.error(request, 'Email Already Registered!')
         return render(request, 'signup.html')

        elif len(username) > 10:
           messages.error(request, 'Username must not exceed 10 characters')
        elif password and password != password2:
           messages.error(request, "Passwords didn't match")
           return render(request, 'signup.html')

        elif not username.isalnum():
           messages.error(request, "Username must be Alpha-Numeric")
           return render(request, 'signup.html')

        myuser = User.objects.create_user(username, email, password)
        myuser.is_active = False
        myuser.save()
        messages.success( request, 'Your account has been successfully created. A confirmation email has been mailed to you please check your email to activate your account')
        #welcome email
        subject = "Welcome to memeshub login"
        message = "Hello, " + myuser.username + "\n" + "Welcome to memeshub!! \n Thank you for visiting our website \n Please confirm your email address in order to activate your account. \n\n Thanking you\n Memeshub, The Best Meme collection site."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        #confirmation email
        current_site = get_current_site(request)
        email_subject = 'Confirm your email @memeshub -Login!'
        email_msg = render_to_string('email_confirmation.html',{
           'username': myuser.username,
           'domain':current_site.domain,
           'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
           'token':generate_token().make_token(myuser)
        })
        email = EmailMessage(
           email_subject,
           email_msg,
           settings.EMAIL_HOST_USER,
           [myuser.email]
        )
        email.fail_silently = True
        email.send()
        return redirect('signIn')

    return render(request, "signup.html")

def activate(request, uidb64, token):
   try:
      uid = force_str(urlsafe_base64_decode(uidb64))
      myuser = User.objects.get(pk=uid)
   except(TypeError, ValueError, OverflowError, User.DoesNotExist):
      myuser = None

   if myuser is not None and generate_token().check_token(myuser, token):
      myuser.is_active = True
      myuser.save()
      login(request, myuser)
      return redirect('homepage')
   else:
      return render(request, 'activation_failed.html')    
   

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def check(request, email):
     if (re.fullmatch(regex, email)):
          # TODO: Add implementation
          pass
     else:
         messages.error(request, "Your email is invalid")
         return render(request, 'signup.html')


def signIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
             login(request, user)
             return redirect('homepage')
        else:
            messages.error(request, 'Credentials do not Match, Check your name and password again. OR check your email to login if you registered')
            return redirect('signIn')

    return render(request, "signIn.html")


def signOut(request):
    logout(request)
    messages.success(request, 'You Have Successfully Logged Out')
    return redirect('homepage')


def about(request):
    return render(request, 'about.html')

def blogs(request):
    return render(request, 'MhBlogs.html')

def privacy(request):
   return render(request, 'privacy.html')


