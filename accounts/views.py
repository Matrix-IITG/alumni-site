from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Profile
from django.db.models import Q

from django.conf import settings

from accounts.forms import EditProfileForm, EditUserForm, CreateProfileForm


def base_response(request, body, title=None, h1=None):
    context_dict = {"base_body": body}
    if title:
        context_dict["base_title"] = title
    if h1:
        context_dict["base_h1"] = h1
    return render(request, "accounts/base.html", context_dict)


def home(request):
    return render(request, "accounts/home.html")


def team(request):
    return render(request, "accounts/team.html")


def about_us(request):
    return render(request, "accounts/about_us.html")


def login_view(request):
    if not request.user.is_authenticated:
        context_dict = {}
        if request.method == "POST":
            next_url = ""
            if "next" in request.POST:
                next_url = request.POST["next"]
            if next_url:
                context_dict["next"] = next_url
            if "username" in request.POST and "password" in request.POST and request.POST["username"] and request.POST[
                "password"]:
                username = request.POST["username"]
                password = request.POST["password"]
                context_dict["username"] = username
                user = authenticate(username=username, password=password)
                if not user:
                    context_dict["login_error"] = "Username or password is incorrect"
                elif not user.is_active:
                    context_dict["login_error"] = "Your account has been disabled. Contact support."
                else:
                    login(request, user)
                    if not next_url:
                        next_url = '/search'
                    return HttpResponseRedirect(next_url)
            else:
                context_dict["login_error"] = "You must enter both username and password"
        elif request.method == "GET":
            if "next" in request.GET and request.GET["next"]:
                context_dict["next"] = request.GET["next"]
        return render(request, "accounts/login.html", context_dict)
    else:
        return HttpResponseRedirect('/search')


def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
    else:
        return base_response(request, "You are already logged out")


def register(request):
    if not request.user.is_authenticated:
        context_dict = {}
        if request.method == "POST":
            keys = ("username", "firstname", "lastname", "password1", "password2")
            if all((key in request.POST and request.POST[key]) for key in keys):
                username = request.POST["username"]
                password1 = request.POST["password1"]
                password2 = request.POST["password2"]
                context_dict["username"] = username
                if password1 != password2:
                    context_dict["register_error"] = "Passwords do not match"
                    form_profile = CreateProfileForm()
                    context_dict["form"] = form_profile
                elif User.objects.filter(username=username).count() > 0:
                    form_profile = CreateProfileForm()
                    context_dict["form"] = form_profile
                    context_dict["register_error"] = "A user with this username already exists"
                else:
                    user = User(username=username)
                    user.set_password(password1)
                    user.first_name = request.POST['firstname']
                    user.last_name = request.POST['lastname']
                    user.email = request.POST["email"]
                    user.save()
                    user = authenticate(username=username, password=password1)
                    print(user.profile.year)
                    form_profile = CreateProfileForm(request.POST, request.FILES, instance=user.profile)
                    if form_profile.is_valid():
                        form_profile.user = user
                        form_profile.save()
                        print("checking location")
                        print(user.profile.pro_img)
                    login(request, user)
                    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            else:
                context_dict["register_error"] = "You must fill out all fields"
        else:
            form_profile = CreateProfileForm()
            context_dict["form"] = form_profile
        return render(request, "accounts/register.html", context_dict)
    else:
        return HttpResponseRedirect('/public_profile')


def account_info(request):
    return render(request, "accounts/account_info.html", {})


def edit_profile(request):
    if request.user.is_authenticated:
        context_dict = {}
        if request.method == "POST":
            form_basic = EditUserForm(request.POST, instance=request.user)
            form_add = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if form_basic.is_valid() and form_add.is_valid():
                form_basic.save()
                form_add.save()
                context_dict["ep_success"] = "Profile changed successsfully"
            else:
                context_dict["ep_error"] = "Invalid data received"
        else:
            form_basic = EditUserForm(instance=request.user)
            form_add = EditProfileForm(instance=request.user.profile)
        context_dict["form_basic"] = form_basic
        context_dict["form_add"] = form_add
        return render(request, "accounts/edit_profile.html", context_dict)
    else:
        return HttpResponseRedirect('/login')


def search(request):
    if request.user.is_authenticated:
        context_dict = {}
        if request.method == "POST":
            if "query" in request.POST and request.POST["query"] != '':
                query = request.POST["query"]
                context_dict["query"] = query
                qur = Q(username__icontains=query) | Q(profile__year__icontains=query) | Q(
                    first_name__icontains=query) | Q(last_name__icontains=query) | Q(
                    profile__curr_work__icontains=query) | Q(profile__prev_work__icontains=query)
                context_dict["result"] = User.objects.filter(Q(is_superuser=False), qur)
                print(context_dict["result"])
                if len(context_dict["result"]) == 0:
                    context_dict["empty"] = "No matching user found for "
                print("hi")
                return render(request, "accounts/search_result.html", context_dict)
            else:
                context_dict["error"] = "You must enter a valid search query"
        return render(request, "accounts/search_result.html", context_dict)
    else:
        return HttpResponseRedirect('/login')


def public_profile(request, username):
    if request.user.is_authenticated:
        puser = get_object_or_404(User, username=username)
        context_dict = {"puser": puser}
        return render(request, "accounts/public_profile.html", context_dict)
    else:
        return HttpResponseRedirect('/login')
