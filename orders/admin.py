from django.contrib import admin
from .models import Order, OrderItems, Coupon
# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItems
    raw_id_fields = ('product',)
    exclude=("price ",)
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'paid', 'updated')
    list_filter = ('paid',)
    inlines = (OrderItemInline,)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'active')