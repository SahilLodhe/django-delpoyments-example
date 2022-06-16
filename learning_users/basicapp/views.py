import imp
from pickletools import read_unicodestring1
from xml.etree.ElementInclude import include
from django import http
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
# FOR MTV
from basicapp.models import UserProfileInfo
from basicapp.forms import UserForm,UserProfileInfoForm
#FOR LOGIN
# from django import reverse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def index(request):
    return render(request,'basicapp/index.html')

def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user # Have a look at the models.py file, in that, the "user" is declared and has a one to one relation with the "User" model which is inbuilt in django, this means that one user can have only one profile

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'basicapp/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
@login_required # This line of code causes the function to be login required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
    

@login_required
def special(request):
    return HttpResponse("You are logged in!")

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') # "get" grabs by the name tag in the html page
        password = request.POST.get('password')

        user = authenticate(username = username,password = password) # built in authentication function

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account is not active!")
        else:
            print("Someone tried to login and failed!")
            print("Username{} and password{}".format(username,password))
            return HttpResponse("Invalid login details!")
    else:
        return render(request,'basicapp/login.html',{})