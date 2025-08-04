from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>', views.CartRemoveView.as_view(), name='cart_remove'),
    path('details/<int:order_id>/', views.OrderDetailsView.as_view(), name='order_detail'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('apply/<int:order_id>/', views.OrderCouponApplyView.as_view(), name='coupon_apply'),
    path('orders/paid/<int:user_id>/', views.PaidOrderView.as_view(), name='paid_orders'),
    path('orders/paid//details/<int:user_id>/<int:order_id>/', views.PaidOrderDetailsView.as_view(), name='paid_orders_details'),
]