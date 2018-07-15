from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView

from .forms import LoginForm, RegistrationForm, GuestForm
from .models import GuestEmail


def guest_registration_view(request):
    form_class = GuestForm(request.POST or None)
    context = {"form": form_class}
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post or None
    if form_class.is_valid():
        email    = form_class.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/registration/")
    return redirect("/registration/")

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        next_get = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_get or next_post
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)

def login_page(request):
    form_class = LoginForm(request.POST or None)
    context = {"form": form_class}
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post
    if form_class.is_valid():
        username = form_class.cleaned_data.get("username")
        password = form_class.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print("User does not exist/User password incorrect.")
    return render(request, "accounts/login.html", context)


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/registration.html'
    success_url = '/login/'

# User = get_user_model()

# def registration_page(request):
#     form_class = RegistrationForm(request.POST or None)
#     context = {"form": form_class}
#     if form_class.is_valid():
#         form.save()
        # print(form_class.cleaned_data)
        # username = form_class.cleaned_data.get("username")
        # email = form_class.cleaned_data.get("email")
        # password = form_class.cleaned_data.get("password")
        # created_user = User.objects.create_user(username, email, password)
    # return render(request, "accounts/registration.html", context)
