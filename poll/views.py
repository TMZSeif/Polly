from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PollForm, OptionForm
from .models import Poll, Options, MyUser
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.datastructures import MultiValueDictKeyError

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = MyUser.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "register/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'localhost:8000',
					'site_name': 'Polly',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="register/password/password_reset.html", context={"password_reset_form":password_reset_form})

# Create your views here.
def home(request):
    return render(request, 'home.html', {})
    
def view_poll(request, id):
    poll = Poll.objects.get(id=id)
    if poll not in request.user.poll_set.all(): return redirect("/")
    if request.method == "POST":
        print(request.POST)
        try:
            poll = Poll.objects.get(id=request.POST["save"])
            question = request.POST[poll.question]
            poll.question = question
            poll.save()
            for option in poll.options_set.all():
                name = request.POST[option.name]
                option.name = name
                option.save()
                print(option.name)
            print(poll.question)
        except MultiValueDictKeyError:
            try:
                Option = Options.objects.get(id=request.POST["delete"])
                Option.delete()
            except:
                poll = Poll.objects.get(id=request.POST["delete-poll"])
                poll.delete()
                return redirect("/view")
    return render(request, 'view-poll.html', {"poll": poll})
    
def view(request):
    polls = Poll.objects.filter(creator=request.user)
    if request.method == "POST":
        id = request.POST["poll"]
        poll = Poll.objects.get(id=id)
        Poll.delete(poll)
    return render(request, 'view.html', {"polls": polls})

def url(request, id):
    return render(request, "url.html", {"id": id})
    
def results(request, id):
    poll = Poll.objects.get(id=id)
    return render(request, "results.html", {"poll": poll})
    
def poll(request, id):
    poll = Poll.objects.get(id=id)
    if request.method == "POST":
        print(request.POST)
        try:
            first_time = False
            option = Options.objects.get(id=request.POST["option"])
            if request.user.options == None:
                first_time = True
            if request.user not in option.myuser_set.all():
                option.votes += 1
                if not first_time:
                    request.user.options.votes -= 1
                    request.user.options.save()
                option.myuser_set.add(request.user)
                print(option.myuser_set.all(), "ASFG")
                print( request.user.options)
            option.save()
        finally:
            return render(request, "poll.html", {"poll": poll})
    return render(request, "poll.html", {"poll": poll})
    
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
                    
            return redirect("/create/" + str(poll.id))
    return render(request, 'create.html', {"poll_form": poll_form, "option_form": option_form})