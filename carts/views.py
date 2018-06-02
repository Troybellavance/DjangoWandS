from django.shortcuts import render, redirect

from wandsproducts.models import Product

from .models import Cart

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # products = cart_obj.products.all()
    # subtotal = 0
    # for x in products:
    #     subtotal += x.price
    # print(subtotal)
    # cart_obj.subtotal = subtotal
    # cart_obj.discounts = 0
    # cart_obj.total = (cart_obj.subtotal-cart_obj.discounts)
    # cart_obj.save()
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
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart:home")
