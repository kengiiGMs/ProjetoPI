from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from .models import User

# Create your views here.

def index(request):
    return render(request, "ecommerce/index.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "ecommerce/login.html", context={
                "message": "E-mail ou senha incorretos."
            })


    return render(request, "ecommerce/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "ecommerce/register.html", context={
                "message", "Passwords must match."
            })
        
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError:
            return render(request, "ecommerce/register.html", context={
                "message": "Esse endereço de email já está em uso."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ecommerce/register.html")

        