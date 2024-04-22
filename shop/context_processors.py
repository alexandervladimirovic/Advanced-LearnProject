from .models import Category


def categories(request):
    """
    Retrieves a list of top-level categories from the database and 
    returns them as a dictionary.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing the top-level categories.
        The keys are 'categories' and the values are a queryset of 
        Category objects.
    """
    categories = Category.objects.filter(parent=None)
    return {
        'categories': categories
    }