from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from admin_panel.models import Product, Cart, CartItem, Order, OrderItem, Category
from django.contrib.admin.views.decorators import staff_member_required

def search(request):
    """Handles product search."""
    query = request.GET.get('q', '').strip()
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, "products_templates/search_results.html", {"query": query, "results": results})

def shop(request, category_id=None):
    """Displays products, filtered by category if selected."""
    categories = Category.objects.all()
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    return render(request, "products_templates/shop.html", {"products": products, "categories": categories})

@login_required
def add_to_cart(request, product_id):
    """Adds a product to the cart or increases quantity if already added."""
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, f"Updated quantity for {product.name}.")
    else:
        messages.success(request, f"Added {product.name} to your cart.")
    return redirect("cart")

@login_required
def view_cart(request):
    """Displays the cart and calculates total price."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    final_total = sum(item.total_price() for item in cart_items)
    return render(request, "products_templates/cart.html", {"cart_items": cart_items, "final_total": final_total})

@login_required
def remove_from_cart(request, item_id):
    """Removes a product from the cart."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    messages.warning(request, f"Removed {cart_item.product.name} from your cart.")
    cart_item.delete()
    return redirect("cart")

@login_required
def update_cart(request, item_id):
    """Updates the quantity of a product in the cart."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"Updated {cart_item.product.name} quantity.")
        else:
            cart_item.delete()
            messages.warning(request, f"Removed {cart_item.product.name} from your cart.")
    return redirect("cart")

@login_required
def checkout(request):
    """Redirects to the payment page before completing order."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect("cart")
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, "products_templates/checkout.html", {"cart_items": cart_items, "total_price": total_price})

@login_required
def fake_payment(request):
    """Simulates payment processing and confirms order."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect("cart")
    total_price = sum(item.total_price() for item in cart_items)
    if request.method == "POST":
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart_items.delete()
        messages.success(request, "Payment successful! Order placed.")
        return redirect("orders")
    return render(request, "products_templates/payment.html", {"total_price": total_price})

@login_required
def orders(request):
    """Displays the user's past orders."""
    user_orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "products_templates/orders.html", {"orders": user_orders})

@staff_member_required
def update_order_status(request, order_id):
    """Allows admin to update the status of an order."""
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ["Order Placed", "Processing", "Shipped", "Out for Delivery", "Delivered"]:
            order.status = new_status
            order.save()
            messages.success(request, "Order status updated successfully.")
        else:
            messages.error(request, "Invalid status update.")
    return redirect("admin_orders")

@login_required
def delete_order(request, order_id):
    """Deletes an order with better error handling."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == "Delivered":
        messages.error(request, "Cannot delete a delivered order.")
    else:
        order.delete()
        messages.success(request, "Order deleted successfully.")
    return redirect("orders")

@login_required
def orders_track(request, order_id):
    """Fetch and display tracking details for a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "products_templates/tracking.html", {"order": order})
