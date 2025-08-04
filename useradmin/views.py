from django.shortcuts import render,get_object_or_404, redirect
from django.views import View
from accounts.models import User,Address
from home.models import Comment, Products
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from orders.models import Order, OrderItems
# Create your views here.
class UserAdminView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin and  request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    def get(self, request):
        return render(request, 'useradmin/admin.html')
    def post(self, request):
        pass
    

class ManageUserAdminView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin and  request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    def get(self,request):
        users = User.subject.all()
        for user in users:
            comments = Comment.objects.filter(user=user)
        return render(request, 'useradmin/manage_users/users.html', {'users':users})
    
class ManageRemoveUserAdminView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin and  request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    def get(self,request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user.is_active :
            messages.error(request, 'this user is already disactive', 'danger')
            return redirect('useradmin:manage_users')
        else:
            user.is_active == False
        user.save()
        return redirect('useradmin:manage_users')
    
class ManageCommentsUserAdminView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin and  request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
        
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        comments = Comment.objects.filter(user=user)
        return render(request, 'useradmin/manage_users/user_comments.html', {'comments':comments , 'user':user})

class ManageCommentsUserDeleteAdminView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin and  request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
        
    def get(self,request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        return redirect('useradmin:manage_comments_users', comment.user.id)
    


class ManageOrdersAdminView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin and  request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
        
    def get(self,request):
        orders = Order.objects.all()
        return render(request, 'useradmin/manage_orders/orders.html', { 'orders':orders})
    


class ManageOrderDetailsAdminView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin and  request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
        
    def get(self,request,order_id):
        order = Order.objects.get(pk=order_id)
        orderitems = OrderItems.objects.filter(order=order)
        return render(request, 'useradmin/manage_orders/orders_details.html', {'orderitems':orderitems, 'order':order})
                


class ManageUserDetailsAdminView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin and  request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
        

    def get(self,request,user_id):
        user = User.subject.get(id=user_id)
        user_addresses = Address.objects.filter(user=user)
        orders = Order.objects.filter(user=user)
        comments = Comment.objects.filter(user=user)
        all_costs=0
        for item in orders:
            all_costs += item.get_total_price()
        usercomments = Comment.objects.filter(user=user)
        return render(request, 'useradmin/manage_users/user_details.html', 
                      {'usercomments':usercomments,'all_costs':all_costs,
                       'orders':orders,'user':user,'user':user, 'user_addresses':user_addresses})
    

class ManageProductsAdminView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin and  request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
        
    def get(self,request):
        products = Products.objects.all()
        return render(request,'useradmin/manage_products/products.html', {'products':products})