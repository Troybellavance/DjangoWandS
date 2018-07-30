from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address

from billing.models import BillingProfile
from wandsproducts.models import Product
from orders.models import Order
from .models import Cart

def cart_detail_view_api(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
             "id": x.id,
             "url": x.get_absolute_url(),
             "name": x.name,
             "price": x.price
             }
             for x in cart_obj.products.all()]
    cart_data = {"products": products,"subtotal": cart_obj.subtotal, "total": cart_obj.total}  #Need strings, ints, etc
    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Product is missing.")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            product_added = False
        else:
            cart_obj.products.add(product_obj)
            product_added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():   #Async with ajax for JS, XML, JSON
            print("Ajax request")
            json_data = {
                "added": product_added,
                "removed": not product_added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data, status=200)
            #return JsonResponse({"message": "Error 400"}, status_code=400)  #Alternate REST
    return redirect("cart:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    address_qs = None
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        is_ready = order_obj.check_order_done()
        if is_ready:
            did_charge, charge_msg = billing_profile.billing_charge(order_obj)
            if did_charge:
                order_obj.mark_as_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                return redirect("cart:success")
            else:
                print(crg_msg)
                return redirect("cart:checkout")
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
    }
    return render(request, "carts/checkout.html", context)


def checkout_complete_view(request):
    return render(request, "carts/checkout-complete.html", {})
