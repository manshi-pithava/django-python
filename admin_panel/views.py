from sqlite3 import IntegrityError

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.shortcuts import get_object_or_404  # Add this import
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from accounts.models import UserProfile
from admin_panel.models import Product,Order
from .models import Category, Feedback, AdminSettings  # Import  models
from .forms import CategoryForm, ProductForm, AdminSettingsForm  # Import Forms





# HELPER FUNCTION: Check if user is admin
def is_admin(user):
    try:
        user_profile = UserProfile.objects.get(user=user)
        return user.is_superuser or user_profile.role == 1
    except UserProfile.DoesNotExist:
        return user.is_superuser


# ADMIN DASHBOARD
@login_required(login_url="login")
def admin_dashboard(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()

    users = User.objects.all()

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'users': users
    }
    return render(request, 'admin_templates/admin_dashboard.html', context)

# CREAT/ADD  NEW USER
@login_required(login_url="login")
def add_user(request):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # Ensuring user is not an admin
            user.save()
            messages.success(request, "User added successfully!")
            return redirect("view_customers")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = UserCreationForm()

    return render(request, "admin_templates/admin_dashboard.html", {"form": form})

# VIEW CUSTOMERS
@login_required(login_url="login")
def view_customers(request):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    customers = User.objects.filter(is_superuser=False)  # Get only customers (non-admin users)
    return render(request, "admin_templates/view_customers.html", {"customers": customers})

# EDIT CUSTOMERS/USERS
@login_required(login_url="login")
def edit_user(request, user_id):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        user.save()
        messages.success(request, "User updated successfully!")
        return redirect("admin_dashboard")  # Redirect to the customers list

    return render(request, "admin_templates/admin_dashboard.html", {"user": user})

# DELETE CUSTOMERS/USERS
@login_required(login_url="login")
def delete_user(request, user_id):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        messages.error(request, "Cannot delete admin users.")
        return redirect("admin_dashboard")

    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect("admin_dashboard")

# ADMIN PRODUCTS
@login_required(login_url="login")
def admin_products(request):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    products = Product.objects.all()  # Fetch all products
    categories = Category.objects.all()  # Fetch all categories
    form = ProductForm()  # Form instance for the modal

    context = {
        "products": products,
        "categories": categories,
        "form": form,
    }
    return render(request, "admin_templates/admin_products.html", context)
# ADD PRODUCTS
@login_required(login_url="login")
def admin_add_products(request):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Product added successfully!")
                return redirect("admin_products")
            except IntegrityError as e:
                messages.error(request, f"Database error: {str(e)}")
        else:
            messages.error(request, f"Failed to add product: {form.errors}")
    else:
        form = ProductForm()

    return render(request, "admin_templates/admin_products.html", {"productForm": form})


# UPDATE PRODUCT
@login_required(login_url="login")
def admin_update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("admin_products")
        else:
            messages.error(request, "Failed to update product. Please check the form.")
    else:
        form = ProductForm(instance=product)
    return render(request, "admin_templates/admin_products.html", {"form": form, "product": product})

# DELETE PRODUCT
@login_required(login_url="login")
def admin_delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("admin_products")

# ADMIN CATEGORIES
@login_required(login_url="login")
def admin_categories(request):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    categories = Category.objects.all()  # Fetch all categories
    return render(request, "admin_templates/admin_categories.html", {"categories": categories})


# ADD CATEGORY
@login_required(login_url="login")

def add_category(request):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
        else:
            messages.error(request, "Invalid category name.")
    return redirect("admin_categories")


# EDIT CATEGORY
@login_required(login_url="login")
def edit_category(request, category_id):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    category = get_object_or_404(Category, id=category_id)  # Fix here

    if request.method == "POST":
        category_name = request.POST.get("category_name")
        if category_name:
            category.name = category_name
            category.save()
            messages.success(request, "Category updated successfully!")
        else:
            messages.error(request, "Invalid category name.")
    return redirect("admin_categories")

# DELETE CATEGORY
@login_required(login_url="login")
def delete_category(request, category_id):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    # Fetch category safely
    category = get_object_or_404(Category, id=category_id)

    # Delete category and show success message
    category.delete()
    messages.success(request, "Category deleted successfully!")

    return redirect("admin_categories")


@login_required
def admin_orders(request):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    orders = Order.objects.all().order_by('-created_at')  # Fetch all orders in descending order
    return render(request, 'admin_templates/admin_orders.html', {'orders': orders})


@login_required(login_url="login")
def update_order_status(request, order_id):
    """Updates the order status safely."""
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("status")

        # Ensure the new status is valid
        valid_statuses = ["Pending", "Out for Delivery", "Delivered", "Cancelled"]
        if new_status not in valid_statuses:
            messages.error(request, "Invalid status selected.")
            return redirect("admin_orders")

        try:
            order.status = new_status
            order.save()
            messages.success(request, f"Order {order.id} status updated to {new_status}.")
        except IntegrityError:
            messages.error(request, "Database error: Foreign key constraint failed!")
        except Exception as e:
            messages.error(request, f"Unexpected error: {str(e)}")

    return redirect("admin_orders")
@login_required(login_url="login")
def delete_order(request, order_id):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Order deleted successfully!")

    return redirect("admin_orders")

# ADMIN FEEDBACK
@login_required(login_url="login")
def admin_feedback(request):
    feedback_list = Feedback.objects.all().order_by('-created_at')  # Fetch all feedback
    return render(request, 'admin_templates/admin_feedback.html', {'feedback_list': feedback_list})

@login_required(login_url="login")
def delete_feedback(request, feedback_id):
    feedback = Feedback.objects.get(id=feedback_id)
    feedback.delete()
    messages.success(request, "Feedback deleted successfully!")
    return redirect('admin_feedback')


# ADMIN ANALYTICS
@login_required(login_url="login")
def admin_analytics(request):
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="Pending").count()
    total_revenue = sum(order.order_items.aggregate(total=models.Sum('product__price'))['total'] or 0 for order in Order.objects.all())

    recent_orders = Order.objects.order_by('-created_at')[:5]  # Last 5 orders

    context = {
        "total_users": total_users,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders,
    }
    return render(request, "admin_templates/admin_analytics.html", context)

# ADMIN SETTINGS
@login_required(login_url="login")
def admin_settings_view(request):
    # Get existing settings or create new one
    settings, created = AdminSettings.objects.get_or_create(id=1)

    if request.method == "POST":
        form = AdminSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect("admin_settings")  # Redirect after saving

    else:
        form = AdminSettingsForm(instance=settings)

    return render(request, "admin_templates/admin_settings.html", {"form": form})
# ADMIN LOGOUT
def admin_logout(request):
    if request.user.is_authenticated:
        messages.success(request, "You have been logged out.")
        logout(request)  # Move logout after the message
    return redirect("index")
