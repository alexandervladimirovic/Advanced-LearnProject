import random
import string

from django.db import models
from django.utils.text import slugify
from django.urls import reverse


def rand_slug():
    """
    Generate a random slug of 3 characters using a combination
    of letters (both lowercase and uppercase) and digits.
    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


class Category(models.Model):
    """
    Represents a category in the shop.
    """
    name = models.CharField('Категория', max_length=200, db_index=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children', verbose_name='Родительская категория', blank=True, null=True
    )
    slug = models.SlugField('URL', max_length=200, unique=True, null=False, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """
        Returns a string representation of the object.

        This method constructs a string representation of the object 
        by traversing the parent-child hierarchy of the object and constructing 
        a full path from the root to the current object. The full path is constructed 
        by concatenating the names of each object in the hierarchy, separated by ' -> '.
        The resulting string is returned.
        """
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])
    

    def save(self, *args, **kwargs):
        """
        Saves the object to the database.
        """

        if not self.slug:
            self.slug = slugify(rand_slug() + 'pickBetter' + self.name)
        return super(Category, self).save(*args, **kwargs)
    

    def get_absolute_url(self):
        """
        Returns the absolute URL of the object by reversing the
        'model_detail' view with the object's primary key as a 
        keyword argument.
        """
        return reverse('shop:category_list', args=[str(self.slug)])


class Product(models.Model):
    """
    Represents a product in the store.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    title = models.CharField('Наименование', max_length=200)
    brand = models.CharField('Бренд', max_length=200)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField('URL', max_length=200)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField('Изображение', upload_to='products/%Y/%m/%d')
    available = models.BooleanField('Наличие', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        

    def __str__(self):
        """
         Returns a string representation of the object.
        """
        return self.title
        
    def get_absolute_url(self):
        """
        Returns the absolute URL of the product detail page for the current product.
        """
        return reverse('shop:product_detail', args=[str(self.slug)])


class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Returns a queryset of available objects.
        """
        return super(ProductManager, self).get_queryset().filter(available=True)



class ProductProxy(Product):

    objects = ProductManager()

    class Meta:
        proxy = True

        



