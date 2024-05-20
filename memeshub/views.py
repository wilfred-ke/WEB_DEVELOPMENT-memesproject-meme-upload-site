from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import ImageForm
from .models import TheProfile, Image, LikeImage, FollowersCount
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .tokens import generate_token
from itertools import chain
from django.core.mail import EmailMessage, send_mail
import os
import re
import random

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

@login_required
def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Image.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('homepage')   
    else:
       form = ImageForm()
    return render(request, 'upload.html', {'form': form})


def index(request):
    if request.method == 'GET':
        if 'q' in request.GET:
            q = request.GET['q']
            multiple_q = Q(Q(caption__icontains=q) | Q(date__icontains=q) | Q(user__icontains=q))
            img = Image.objects.filter(multiple_q)
            
            # Check if any results were found
            if not img:
                messages.info(request, f"No results found for '{q}'.")
        else:
            img = Image.objects.all().order_by('-date')

    else:
        img = Image.objects.all().order_by('-date')

    user_profile = None
    if request.user.is_authenticated:
        try:
            user_object = User.objects.get(username=request.user.username)
            user_profile = TheProfile.objects.get(user=user_object)
        except TheProfile.DoesNotExist:
            # If the user profile doesn't exist, use the default profile
            user_profile = TheProfile.objects.get(profileimg=True)

    return render(request, 'index.html', {'img': img, 'user_profile': user_profile})

@login_required
def LikeView(request, pk):
   if request.user.is_authenticated:
      meme = get_object_or_404(Image, id=request.POST.get('meme_id'))

      # Check if the user has already disliked the post
      if meme.dislikes.filter(id=request.user.id):
         messages.warning(
             request, 'You cannot like and dislike the same meme.')
         return HttpResponseRedirect(reverse('page'))

      if meme.likes.filter(id=request.user.id):
         meme.likes.remove(request.user)
      else:
          meme.likes.add(request.user)

      return HttpResponseRedirect(reverse('page'))

   # Handle the case when the user is not authenticated
   messages.success(request, 'You must be logged in to like this meme.')
   return HttpResponseRedirect(reverse('page'))


@login_required
def DislikeView(request, pk):
   if request.user.is_authenticated:
      meme = get_object_or_404(Image, id=request.POST.get('meme_id'))

      # Check if the user has already liked the meme
      if meme.likes.filter(id=request.user.id):
         messages.warning(
             request, 'You cannot like and dislike the same meme.')
         return HttpResponseRedirect(reverse('page'))

      if meme.dislikes.filter(id=request.user.id):
         meme.dislikes.remove(request.user)
      else:
         meme.dislikes.add(request.user)

        # Redirect back to the previous page or a specific URL
      return HttpResponseRedirect(reverse('page'))

    # Handle the case when the user is not authenticated
   messages.success(request, 'You must be logged in to dislike this meme.')
   # You may want to redirect to the login page or a specific URL
   return HttpResponseRedirect(reverse('page'))


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

        # create a profile object for new user
        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()

        #welcome email
        subject = "Welcome to TrendWave login"
        message = "Hello, " + myuser.username + "\n" + "Welcome to TrendWave!! \n Thank you for visiting our website \n Please confirm your email address in order to activate your account. \n\n Thanking you\n TrendWave - Ride the Wave of Trends."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        #confirmation email
        current_site = get_current_site(request)
        email_subject = 'Confirm your email @TrendWave -Login!'
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

# @login_required(login_url='signin')
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


def custom_logout(request):
    if request.user.is_authenticated:
        username = request.user.username
        request.session['username'] = username

    # Perform logout
    logout(request)

    # Check if the session variable exists before deleting it
    if 'username' in request.session:
        del request.session['username']

    messages.success(request, 'You have successfully logged out.')
    return redirect('homepage')



def about(request):
    return render(request, 'about.html')

def blogs(request):
    return render(request, 'MhBlogs.html')

def privacy(request):
   return render(request, 'privacy.html')

@login_required
def user_settings(request):
   user_profile = TheProfile.objects.get(user=request.user)

   if request.method == 'POST':
      image = request.FILES.get('image')
      bio = request.POST.get('bio')
      location = request.POST.get('location')

      if image:
         user_profile.profileimg = image
      if bio:
         user_profile.bio = bio
      if location:
         user_profile.location = location

      user_profile.save()
      return redirect('user_settings')      

   return render(request, 'user_settings.html', {'user_profile': user_profile})


@login_required
def like_image(request):
   username = request.user.username
   image_id = request.GET.get('x_id')

   image = Image.objects.get(id=image_id)

   like_filter = LikeImage.objects.filter(image_id=image_id, username=username).first()

   if like_filter == None:
      new_like = LikeImage.objects.create(image_id=image_id, username=username)
      new_like.save()
      image.likes = image.likes + 1
      image.save()
      return redirect('homepage')
   else:
      like_filter.delete()
      image.likes = image.likes - 1
      image.save()
      return redirect('homepage')


def profile(request, pk):
    user_object = get_object_or_404(User, username=pk)
    user_profile = get_object_or_404(TheProfile, user=user_object)
    user_posts = Image.objects.filter(user=user_object)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
       button_text = 'UnFollow'
    else:
       button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following,
    }
    return render(request, 'profile.html', context)


def robots(request):
   return render(request, 'robots.txt')

@login_required
def follow(request):
   if request.method == 'POST':
      follower = request.POST['follower']
      user = request.POST['user']

      if FollowersCount.objects.filter(follower=follower, user=user).first():
         delete_follower = FollowersCount.objects.get(follower=follower, user=user)
         delete_follower.delete()
         return redirect('/profile/'+user)
      else:
         new_follower = FollowersCount.objects.create(follower=follower, user=user)
         new_follower.save()
         return redirect('/profile/'+user)
   else:
      return redirect('/')
   
# feed for user and user_following
@login_required   
def following(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = TheProfile.objects.get(user=user_object)
    user_following_list = []
    feed = []
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    
    for users in user_following:
        user_following_list.append(users.user)

    if user_following_list:  # Check if the user is following anyone
        for usernames in user_following_list:
            feed_lists = Image.objects.filter(user=usernames)
            feed.append(feed_lists)
        feed_list = list(chain(*feed))
    else:
        feed_list = []  # Ensure feed_list is assigned an empty list if no following users

    # User suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if x not in list(user_following_all)]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if x not in list(current_user)]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []
    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = TheProfile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'following.html', {
        'feed_list': feed_list,
        'user_profile': user_profile,
        'suggestions_username_profile_list': suggestions_username_profile_list
    })

# def search_user_query(request):
   # user_object = User.objects.get(username=request.user.username)
   # user_profile = TheProfile.objects.get(user=user_object)
   # if request.method == 'POST':
      # username = request.POST['username']
      # username_object = User.objects.filter(username__icontains=username)

      # username_profile = []
      # username_profile_list = []

      # for users in username_object:
         # username_profile.append(users.id)

      # for ids in username_profile:
         # profile_lists = TheProfile.objects.filter(id_user=ids)
         # username_profile_list.append(profile_lists)

      # username_profile_list = list(chain(*username_profile_list))      

   # return render(request, 'following.html', {'user_profile':user_profile,# 'username_profile_list':username_profile_list})   