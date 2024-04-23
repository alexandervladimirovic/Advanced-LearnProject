from decimal import Decimal

from shop.models import ProductProxy


class Cart:

    def __init__(self, request) -> None:
        """
        Initializes a new instance of the Cart class.

        Initializes the session attribute with the session object
        from the request. Retrieves the value of the "session_key" key 
        from the session object. If the value is None, sets the 
        "session_key" key in the session object to an empty dictionary.
        Assigns the retrieved or created cart dictionary to the cart 
        attribute.
        """

        self.session = request.session

        cart = self.session.get("session_key")

        if not cart:
            cart = self.session["session_key"] = {}

        self.cart = cart


    def __len__(self):
        """
        Calculates the total count of items in the cart based on the 
        quantity of each item.
        Returns the total count as an integer.
        """
        return sum(item["quantity"] for item in self.cart.values())


    def __iter__(self):
        """
        Iterates over the items in the cart and yields a dictionary for each item.
        
        Yields:
            dict: A dictionary containing information about each item in the cart.
                The dictionary has the following keys:
                - 'product' (ProductProxy): The product object associated with the item.
                - 'price' (Decimal): The price of the item.
                - 'quantity' (int): The quantity of the item.
                - 'total_price' (Decimal): The total price of the item (price * quantity).
        """
        product_ids = self.cart.keys()
        products = ProductProxy.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item



    def add(self, product, quantity):
        """
        Adds a product to the cart.
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": quantity, "price": str(product.price)}

        self.cart[product_id]['quantity'] = quantity

        self.session.modified = True 


    def delete(self, product):
        """
        Deletes a product from the cart.

        Args:
            product (ProductProxy): The product to be deleted.
            quantity (int): The quantity of the product to be deleted.

        This function deletes a product from the cart by removing 
        it from the `self.cart` dictionary. It first converts the `product.id` to a string and checks if it 
        exists in the `self.cart` dictionary. If it does, the product 
        is deleted from the dictionary and the `self.session.modified` 
        flag is set to True.

        Note: This function assumes that the `self.cart` dictionary 
        is a dictionary where the keys are strings representing the 
        product IDs and the values are dictionaries containing the 
        quantity and price of the product.
        """
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True


    def update(self, product, quantity):
        """
        Updates the quantity of a product in the cart.

        Args:
            product: The product to be updated.
            quantity: The new quantity of the product.

        This function updates the quantity of a product in the cart.
        It first converts the product ID to a string and then checks 
        if the product exists in the cart. If it does, the quantity 
        of the product is updated, and the session modification flag 
        is set to True.
        """

        product_id = str(product)

        if product_id in self.cart:
            self.cart[product_id]["quantity"] = quantity
            self.session.modified = True




    def get_total_price(self):
        """
        Calculates and returns the total price of all items in the cart.

        Returns:
            Decimal: The total price of all items in the cart.
        """
        return sum(
            Decimal(item['price']) * item['quantity'] 
            for item in self.cart.values())


            