from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .forms import ContactForm

def home_page(request):
    #print(request.session.get("first_name", "Unknown")) #get
    # request.session['first_name']
    context = {
        "title":"Hello!",
        "content":"Welcome to the home page of Walrus & Sons!",
    }
    if request.user.is_authenticated():
        context["premium_content"] = "Members added into a monthly premium wallet salmon drawing!"
    return render(request, "home_page.html", context)


def about_page(request):
    context = {
        "title":"About Walrus & Sons:",
        "content":"A company spanning several generations!"
    }
    return render(request, "about/about_page.html", context)

def contact_page(request):
    form_class = ContactForm(request.POST or None)
    context = {
        "title":"Contact Walrus & Sons:",
        "content":"Where we work to insure all your walrus needs are met!",
        "form": form_class
        }
    if form_class.is_valid():
        print(form_class.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message": "Walrus & Sons thanks you for your submission!"})

    if form_class.errors:
        errors = form_class.errors.as_json()
        print(form_class.cleaned_data)
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    return render(request, "contact/contact_page.html", context)
