from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import stripe
stripe.api_key = "sk_test_lhe3uvwYErAh2ECdCfg6YD3C"
STRIPE_PUBLIC_KEY = 'pk_test_E06fqQ0w0Yh0gNtiUmRjPg9o'

def payment_method_view(request):
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUBLIC_KEY})


def payment_method_createview(request):
    if request.method == "POST":
        print(request.POST)
        return JsonResponse({"message": "Finished"})
    return HttpResponse("error", status_code=401)
