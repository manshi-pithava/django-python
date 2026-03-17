from django.urls import path
from . import views


urlpatterns = [
    path("shop/", views.shop, name="shop"),
    path("shop/category/<int:category_id>/", views.shop, name="shop_by_category"),
    path("cart/", views.view_cart, name="cart"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path("checkout/", views.checkout, name="checkout"),
    path('payment/', views.fake_payment, name='payment'),  # ✅ Payment Simulation
    path('orders/', views.orders, name='orders'),
    path('order_track/<int:order_id>/', views.orders_track, name='order_track'),
path('search/', views.search, name='search'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
]
