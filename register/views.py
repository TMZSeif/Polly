from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(response, user)
            print(response.user)
            return redirect('/')
        
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})