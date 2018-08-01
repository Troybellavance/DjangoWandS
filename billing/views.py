from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_lhe3uvwYErAh2ECdCfg6YD3C")
STRIPE_PUBLIC_KEY = getattr(settings, "STRIPE_PUBLIC_KEY", "pk_test_t0959FwEVWMRzwKLOrwPJeqI")
stripe.api_key = STRIPE_SECRET_KEY

from .models import BillingProfile, CreditCard


def payment_method_view(request):
    # if request.user.is_authenticated():
    #     billing_profile = request.user.billingprofile
    #     customer_id = billing_profile.customer_id
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart")
    next_url = None
    next_get = request.GET.get('next')
    if is_safe_url(next_get, request.get_host()):
        next_url = next_get
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUBLIC_KEY, "next_url": next_url})


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user."}, status_code=401)
        token = request.POST.get("token")
        if token is not None:
            new_card_obj = CreditCard.objects.add_new_stripe(billing_profile, token)
        return JsonResponse({"message": "Your card was successfully added."})
    return HttpResponse("error", status_code=401)
