from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm, RegistrationForm

# Create your views here.

def login_page(request):
    form_class = LoginForm(request.POST or None)
    context = {"form": form_class}
    #print(request.user.is_authenticated())
    if form_class.is_valid():
        print(form_class.cleaned_data)
        username = form_class.cleaned_data.get("username")
        password = form_class.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            #print(request.user.is_authenticated())
            login(request, user)
            # Redirect to a success page.
            #context['form'] = LoginForm()
            return redirect("/login")
        else:
            # Return an 'invalid login' error message.
            print("User does not exist/User password incorrect.")
    return render(request, "accounts/login.html", context)

User = get_user_model()
def registration_page(request):
    form_class = RegistrationForm(request.POST or None)
    context = {"form": form_class}
    if form_class.is_valid():
        print(form_class.cleaned_data)
        username = form_class.cleaned_data.get("username")
        email = form_class.cleaned_data.get("email")
        password = form_class.cleaned_data.get("password")
        created_user = User.objects.create_user(username, email, password)
    return render(request, "accounts/registration.html", context)
