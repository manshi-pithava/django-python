from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Category(models.Model):
    """Represents a product category."""
    name = models.CharField(max_length=255, unique=True)  # Category name must be unique

    def __str__(self):
        return self.name


class Product(models.Model):  # Keeping the model name as Product
    """Represents a product in the store."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    """Represents a shopping cart for a user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    """Represents an individual item in a cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Keeping Product model name as is
    quantity = models.PositiveIntegerField(default=1)  # Ensure quantity is always at least 1

    def total_price(self):
        return Decimal(self.product.price) * self.quantity  # Use Decimal to prevent rounding issues

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Order(models.Model):
    """Represents an order placed by a user."""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Added total_price field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    """Represents an item within an order."""
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Keeping Product model name as is
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"



class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name}"




class AdminSettings(models.Model):
    admin_email = models.EmailField(default="admin@example.com")
    site_name = models.CharField(max_length=255, default="E-Shop")
    site_url = models.URLField(default="http://127.0.0.1:8000")
    enable_2fa = models.BooleanField(default=True)
    allow_admin_registration = models.BooleanField(default=False)
    session_timeout = models.PositiveIntegerField(default=30)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return self.site_name