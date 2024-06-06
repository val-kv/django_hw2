from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active_version_name = models.CharField(max_length=50, default="No active version")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

        permissions = [
            ('cancel_product_publication', 'Can cancel product publication'),
            ('change_product_description', 'Can change product description'),
            ('change_product_category', 'Can change product category'),
        ]


class BlogPost(models.Model):
    title: str = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    preview = models.ImageField(upload_to='previews/')
    created_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version_number = models.CharField(max_length=50)
    version_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def clean(self):
        if self.is_active and Version.objects.filter(product=self.product, is_active=True).exclude(
                id=self.id).exists():
            raise ValidationError('Only one version can be the current version for a product.')

    def __str__(self):
        return f"{self.product.name} - {self.version_number} ({self.version_name})"
