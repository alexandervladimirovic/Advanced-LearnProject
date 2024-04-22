from django.shortcuts import render, get_object_or_404

from .models import Category, ProductProxy



def products_view(request):
    """
    Renders the 'shop/products.html'
    template with a context containing all products.
    """
    products = ProductProxy.objects.all()
    return render(request, 'shop/products.html', {'products': products})

def product_detail_view(request, slug):
    """
    Renders the 'shop/product_detail.html' template with
    a context containing the product with the specified slug.
    """
    product = get_object_or_404(ProductProxy, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

def category_list(request, slug):
    """
    Retrieves a category based on the provided slug, fetches all products associated
    with that category, and renders the 'shop/category_list.html' template with the category
    and products in the context.
    """
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/category_list.html', context)



