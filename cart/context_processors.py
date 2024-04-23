from .cart import Cart


def cart(request):
    """
    Initializes and returns a dictionary containing a Cart object.

    Returns:
        dict: A dictionary with a single key-value pair. 
        The key is 'cart' and the value is a Cart object initialized 
        with the given request.
    """
    return{'cart': Cart(request)}