from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from shop.models import ProductProxy
from .cart import Cart


def cart_view(request):
    """
    A view function that renders the cart view.
    """
    cart = Cart(request)

    context = {
        'cart':cart
    }

    return render(request, 'cart/cart-view.html', context)


def cart_add(request):
    """
    Adds a product to the cartю

    Returns:
        JsonResponse: A JSON response containing the quantity of 
        items in the cart and the title of the added product.
    """
    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(ProductProxy, id=product_id)

        cart.add(product=product, quantity=product_quantity)

        cart_quantity = cart.__len__()

        responce = JsonResponse({'quantity': cart_quantity, 'product': product.title})

        return responce





def cart_delete(request):
    """
    Deletes a product from the cart based on the provided request.
    """
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product = product_id)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total_price()
        responce = JsonResponse({'quantity': cart_quantity, 'total': cart_total})

        return responce


def cart_update(request):
    """
    Updates the cart with the given product and quantity.

    Returns:
        JsonResponse: A JSON response containing the updated cart 
        quantity and total price.
    """
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        cart.update(product = product_id, quantity = product_quantity)

        cart_quantity = cart.__len__()
        cart_total = cart.get_total_price()
       
        responce = JsonResponse(
            {'quantity': cart_quantity, 'total': cart_total})

        return responce
