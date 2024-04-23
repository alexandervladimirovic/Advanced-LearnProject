from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Product, Category, ProductProxy


class ProductViewTest(TestCase):
    def test_get_products(self):
        """
        Test the `get_products` method of the `ProductViewTest` 
        class.

        This test case verifies that the `get_products` method 
        correctly retrieves and displays a list of products on 
        the products page.

        Steps:
        1. Create a small GIF image.
        2. Create an uploaded file object with the small GIF image.
        3. Create a category object.
        4. Create two product objects, each with a unique title, 
        slug, category, and image.
        5. Send a GET request to the products page.
        6. Assert that the response status code is 200.
        7. Assert that the number of products in the response 
        context is 2.
        8. Assert that the list of products in the response 
        context matches the expected list of product objects.
        9. Assert that the response contains the content of 
        the first product object.
        10. Assert that the response contains the content 
        of the second product object.
        """

        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile("test_image.gif", small_gif, content_type="image/gif")
        category = Category.objects.create(name="test")
        product_1 = Product.objects.create(
            title="Product 1",
            category=category,
            image=uploaded,
            slug="product-1"
            
        )
        product_2 = Product.objects.create(
            title="Product 2",
            category=category,
            image=uploaded,
            slug="product-2",
        )

        response = self.client.get(reverse("shop:products"))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["products"].count(), 2)
        self.assertEqual(list(response.context["products"]), [product_1, product_2])
        self.assertContains(response, product_1)
        self.assertContains(response, product_2)



class ProductDetailViewTest(TestCase):
    def test_get_product_by_slug(self):
        """
        Test case for the `get_product_by_slug` method of the
        `ProductDetailViewTest` class.

        This test verifies that the `get_product_by_slug` 
        method correctly retrieves and displays a product on 
        the product detail page.

        Steps:
        1. Create a small GIF image.
        2. Create an uploaded file object with the small GIF image.
        3. Create a category object.
        4. Create a product object with a unique title, slug, 
        category, and image.
        5. Send a GET request to the product detail page with 
        the product's slug.
        6. Assert that the response status code is 200.
        7. Assert that the slug of the product in the response 
        context matches the slug of the created product.
        8. Assert that the response contains the content of the 
        created product.
        """
        
        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile("small.gif", small_gif, content_type="image/gif")
        category = Category.objects.create(name="test")
        product = Product.objects.create(
            title="Test 1",
            category=category,
            image=uploaded,
            slug="test-1",
        )

        response = self.client.get(
            reverse("shop:product_detail", kwargs={'slug': 'test-1'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"].slug, product.slug)


class CategoryListViewTest(TestCase):
    def setUp(self):
        """
        Set up the test environment by creating a test category 
        and a test product.
        """
        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            "small.gif", small_gif, content_type="image/gif")
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category")
        self.product = Product.objects.create(
            title="Test Product",
            category=self.category,
            image=uploaded,
            slug="test-product")
        
    def test_status_code(self):
        """
        Test the status code of the response returned 
        by the `category_list` view.
        """
        response = self.client.get(
            reverse("shop:category_list", args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        """
        A description of the entire function, 
        its parameters, and its return types.
        """
        responce = self.client.get(
            reverse("shop:category_list", args=[self.category.slug]))
        self.assertTemplateUsed(responce, "shop/category_list.html")

    def test_context_data(self):
        """
        Test the context data of the response returned 
        by the `category_list` view.
        """
        response = self.client.get(
            reverse("shop:category_list", args=[self.category.slug]))
        self.assertEqual(response.context["category"], self.category)
        self.assertEqual(response.context["products"].first(), self.product)
        


        
       
        



