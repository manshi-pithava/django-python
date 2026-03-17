from django.urls import path
from .import views

urlpatterns = [
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("view-customers/", views.view_customers, name="view_customers"),
    path("edit-user/<int:user_id>/", views.edit_user, name="edit_user"),
    path("delete-user/<int:user_id>/", views.delete_user, name="delete_user"),
    path("add-user/", views.add_user, name="add_user"),


    # Products
    path("admin-products/", views.admin_products, name="admin_products"),
    path("admin-add-product/", views.admin_add_products, name="admin_add_product"),  # Singular name
    path("admin-update-product/<int:product_id>/", views.admin_update_product, name="admin_update_product"),
    path("admin-delete-product/<int:product_id>/", views.admin_delete_product, name="admin_delete_product"),

    # Categories
    path("admin-categories/", views.admin_categories, name="admin_categories"),
    path("add-category/", views.add_category, name="add_category"),
    path("edit-category/<int:category_id>/", views.edit_category, name="edit_category"),  # Added ID
    path("delete-category/<int:category_id>/", views.delete_category, name="delete_category"),  # Added ID

    # Orders

    path("admin/orders/", views.admin_orders, name="admin_orders"),
    path("admin/orders/update/<int:order_id>/", views.update_order_status, name="update_order_status"),
    path("admin/orders/delete/<int:order_id>/", views.delete_order, name="delete_order"),


# Other
    path('admin/feedback/', views.admin_feedback, name='admin_feedback'),
    path('admin/feedback/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    path('admin/analytics/', views.admin_analytics, name='admin_analytics'),
    path("admin/settings/", views.admin_settings_view, name="admin_settings"),
    path("logout/", views.admin_logout, name="logout"),
]
