import json

from django.contrib.sessions.middleware import SessionMiddleware

from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from shop.models import Category, ProductProxy

from .views import cart_add, cart_delete, cart_update, cart_view




class CartViewTest(TestCase):

    def setUp(self):
        """
        Set up the test environment by creating a client object,
        a request factory object, a session middleware object, and 
        a session. The client object is used to make HTTP requests,
        the request factory object is used to generate HTTP requests,
        the session middleware object is used to process 
        session-related middleware, and the session is used to 
        store session data. This method is typically called before 
        each test case to ensure a clean test environment.
        """
        self.client = Client()
        self.factory = RequestFactory().get(reverse('cart:cart-view'))
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_view(self):
        """
        Test the cart view by making a request to it and checking 
        the response status code and template used.
        """
        request = self.factory
        responce = cart_view(request)
        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(self.client.get(reverse('cart:cart-view')), 'cart/cart-view.html')


class CartAddViewTestCase(TestCase):

    def setUp(self):
        """
        Set up the test environment by creating a category and 
        a product, and then creating a request factory object with 
        a POST request to the 'cart:add-to-cart' URL with the 
        necessary parameters. The session middleware object is 
        used to process session-related middleware, and the session 
        is used to store session data. This method is typically 
        called before each test case to ensure a clean test 
        environment.
        """
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product', price=10.0, category=self.category)
        self.factory = RequestFactory().post(reverse('cart:add-to-cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_quantity': 2,
        })
        self.middleware  = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_add(self):
        """
        Test the cart_add function.

        This function tests the functionality of the cart_add 
        function by creating a request object using the 
        RequestFactory, then calling the cart_add function with 
        the request object. It asserts that the response status 
        code is 200 and that the 'product' key in the response 
        content is equal to 'Example Product' and the 'quantity' 
        key is equal to 2.
        """
        request = self.factory
        response = cart_add(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['product'], 'Example Product')
        self.assertEqual(data['quantity'], 2)


class CartDeleteViewTestCase(TestCase):

    def setUp(self):
        """
        Set up the test environment by creating a category and 
        a product, and then creating a request factory object with 
        a POST request to the 'cart:delete-to-cart' URL with the 
        necessary parameters. The session middleware object is used 
        to process session-related middleware, and the session is 
        used to store session data. This method is typically called 
        before each test case to ensure a clean test environment.
        """
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product', price=10.0, category=self.category)

        self.factory = RequestFactory().post(reverse('cart:delete-to-cart'), {
            'action': 'post',
            'product_id': self.product.id,
        })
        self.middleware  = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_delete(self):
        """
        Test the cart_delete function.

        This function tests the functionality of the cart_delete 
        function by creating a request object using the RequestFactory,
        then calling the cart_delete function with the request object. 
        It asserts that the response status code is 200 and that 
        the 'quantity' key in the response content is equal to 0.
        """
        request = self.factory
        response = cart_delete(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['quantity'], 0)


class CartUpdateViewTestCase(TestCase):

    def setUp(self):
        """
        Set up the test environment by creating a category, a product, 
        and request factory objects with POST requests to 
        'cart:add-to-cart' and 'cart:update-to-cart' URLs with 
        necessary parameters. Initialize a session middleware object, 
        process the request, and save the session.
        """
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product', price=10.0, category=self.category)
        self.factory = RequestFactory().post(reverse('cart:add-to-cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_quantity': 2,
        })
        self.factory = RequestFactory().post(reverse('cart:update-to-cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_quantity': 5,
        })
        self.middleware  = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_update(self):
        """
        A test function to update the cart. 
        It makes requests to 'cart:add-to-cart' and 
        'cart:update-to-cart' URLs with necessary parameters. 
        It then checks if the response status code is 200 and 
        verifies the total and quantity values in the response data.
        """
        request = self.factory
        response = cart_add(request)
        response = cart_update(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['total'], '50.00')
        self.assertEqual(data['quantity'], 5)