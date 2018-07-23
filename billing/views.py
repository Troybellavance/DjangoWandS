from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.http import is_safe_url

import stripe

stripe.api_key = "sk_test_lhe3uvwYErAh2ECdCfg6YD3C"
STRIPE_PUBLIC_KEY = 'pk_test_E06fqQ0w0Yh0gNtiUmRjPg9o'

def payment_method_view(request):
    next_url = None
    next_get = request.GET.get('next')
    if is_safe_url(next_get, request.get_host()):
        next_url = next_get
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUBLIC_KEY, "next_url": next_url})


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        return JsonResponse({"message": "Your card was successfully added."})
    return HttpResponse("error", status_code=401)
