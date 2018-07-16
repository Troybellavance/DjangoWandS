from django.shortcuts import render

import stripe
stripe.api_key = ""
STRIPE_PUBLIC_KEY = ''

def payment_method_view(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUBLIC_KEY})
