from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PollForm, OptionForm
from .models import Poll, Options

# Create your views here.
def home(request):
    return render(request, 'home.html', {})
    
def create(request):
    poll_form = PollForm()
    option_form = OptionForm()
    if request.method == "POST":
        poll_form = PollForm(request.POST["question"])
        if poll_form.is_valid:
            poll = Poll(question=request.POST["question"], creator=request.user)
            poll.save()
            options = request.POST.getlist("options")
            for option in options:
                print(option)
                print(request.POST)
                print(request.POST.getlist("options"))
                option_form = OptionForm(option)
                if option_form.is_valid:
                    poll.options_set.create(name=option)
                    
            return redirect("/")
    return render(request, 'create.html', {"poll_form": poll_form, "option_form": option_form})