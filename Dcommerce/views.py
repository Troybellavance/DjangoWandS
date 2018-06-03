from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegistrationForm


def home_page(request):
    #print(request.session.get("first_name", "Unknown")) #get
    # request.session['first_name']
    context = {
        "title":"Hello!",
        "content":"Welcome to the home page of Walrus & Sons!",
    }
    if request.user.is_authenticated():
        context["premium_content"] = "Bonus wallet salmon."
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
        "content":"Where all of your walrus related questions will be answered!",
        "form": form_class
        }
    if form_class.is_valid():
        print(form_class.cleaned_data)
    # if request.method == "POST":
    #     #print(request.POST)
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))
    return render(request, "contact/contact_page.html", context)


# def home_page_old(request):
#     html_ = """
#     <!doctype html>
#     <html lang="en">
#       <head>
#         <!-- Required meta tags -->
#         <meta charset="utf-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
#
#         <!-- Bootstrap CSS -->
#         <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
#
#         <title>Hello, world!</title>
#       </head>
#       <body>
#         <h1>Hello, world!</h1>
#
#         <!-- Optional JavaScript -->
#         <!-- jQuery first, then Popper.js, then Bootstrap JS -->
#         <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
#         <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
#         <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
#       </body>
#     </html>
#     """
#     return HttpResponse(html_)
