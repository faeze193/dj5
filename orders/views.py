from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .forms import CartAddForm , CouponForm
from .carts import Cart
from home.models import Products
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order,OrderItems, Coupon
from django.contrib import messages
import datetime
from accounts.models import User

class CartView(View):
    def get(self,request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart':cart})
    

class CartAddView(View):
    
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Products, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('home:product_details', product.slug)
    

class CartRemoveView(View):
    def get(self,request,product_id):
        cart = Cart(request)
        product = get_object_or_404(Products, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')

class OrderDetailsView(LoginRequiredMixin, View):
    
    form_class = CouponForm

    def get(self,request,order_id):
        order = get_object_or_404(Order,id=order_id)
        return render(request,'orders/checkout.html', {'order':order, 'form':self.form_class})
        


class OrderCreateView(LoginRequiredMixin,View):
    
    def get(self,request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItems.objects.create(order=order,product=item['product'],
                                          price=item['price'],quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order_detail', order.id)
    

class OrderCouponApplyView(LoginRequiredMixin, View):

    form_class = CouponForm

    def post(self, request, order_id):
        form = self.form_class(request.POST)
        now = datetime.datetime.now()
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_detail', order_id)
    

class PaidOrderView(LoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        if kwargs['user_id']==request.user.id:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('home:home')

    def get(self,request, user_id):
        user = User.subject.get(id=user_id)
        orders = Order.objects.filter(user=user)
        return render(request, 'orders/paid_orders.html', {'orders':orders})
        


class PaidOrderDetailsView(View):
    def dispatch(self, request, *args, **kwargs):
        if kwargs['user_id']==request.user.id:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('home:home')
    def get(self,request,user_id,order_id):
        orderitems = OrderItems.objects.filter(order=order_id)
        order = Order.objects.get(pk=order_id)
        return render(request, 'orders/paid_order_details.html', {'orderitems':orderitems, 'order':order})
                
