from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Products, Category, Comment
from . import tasks
from django.contrib import messages
from utils import IsAdminMixin
from .forms import UploadObjectBucketForm 
from .forms import CommentForm, ProductColorForm
from django.core.files.uploadedfile import SimpleUploadedFile
from orders.forms import CartAddForm
from django.db.models import Q
from django.http import JsonResponse
from accounts.form import UserRegisterPhoneForm , UserRegisterCodeForm
from .forms import SearchForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Advertisement
#from .models import PromoBanner


# Create your views here.




    

class ProductsSearchView(View):

    def get(self,request):
        form = SearchForm(request.GET)
        productst = Products.objects.all()  # ابتدا همه محصولات را دریافت کنید

        if form.is_valid():
            query = form.cleaned_data['q']
            # استفاده از Q object برای جستجو در چند فیلد
            products = products.filter(
                Q(name__icontains=query) | Q(descriptions__icontains=query)
            )

        return render(request, 'home/q_products.html', {
            'form': form,
            'products': products
        })



class HomeView(View):

    def get(self, request, category_slug=None):
        products = Products.objects.all()
        categories = Category.objects.filter(is_sub=False)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(products, 5)  # نمایش 10 محصول در هر صفحه
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        #ads
        active_ads = Advertisement.objects.filter(is_active=True).order_by('-created_at')[:5] # مثلاً 5 تبلیغ آخر فعال
        
        advertisements = active_ads
        # ... other context variables

        #promo banner
        #promo_banners = PromoBanner.objects.filter(is_active=True)
        
    
        
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/index.html', {'products':products,
                                                   'categories':categories,
                                                    'advertisements':advertisements,
                                                      })
    
    

class ProductDitailsView(View):

    def get(self, request, slug):
        product = get_object_or_404(Products, slug=slug)
        colors = product.product_colors.all()
        sub_category = product.category.get(is_sub=True)
        top_category = product.category.get(is_sub=False)
        comments = Comment.objects.filter(product=product)
        
        form = CartAddForm
        comment_form = CommentForm
        color_form = ProductColorForm

        total = 0
        for comment in comments:
            total += 1
        return render(request, 'home/product_details.html', {'product':product,
                    'sub_category':sub_category,'top_category':top_category,
                    'comments':comments,'total':total ,'form':form, 'comment_form':comment_form,
                    'colors':colors,'comment_form':comment_form,'color_form':color_form})

class LikeCommentView(View):
    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        user = request.user
        if user in comment.likes.all():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True
        return JsonResponse({'liked': liked, 'likes_count': comment.likes.count()})

class DisLikeCommentView(View):
    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        user = request.user
        if user in comment.dislikes.all():
            comment.dislikes.remove(user)
            disliked = False
        else:
            comment.dislikes.add(user)
            disliked = True
        return JsonResponse({'disliked': disliked, 'dislikes_count': comment.dislikes.count()})


        
    
    
    

class BucketHomeView(IsAdminMixin,View):

    def get(self, request):
        object_list = tasks.get_all_task()
        return render(request, 'home/bucket.html', {'object_list':object_list})
      


class DeleteObjectBucketView(IsAdminMixin,View):

    def get(self,request,key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'deleted successully', 'success')
        return redirect('home:bucket_home')
    



class DownloadObjectBucketView(IsAdminMixin,View):

    def get(self,request,key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'downloaded successully', 'success')
        return redirect('home:bucket_home')
    

class UploadObjectBucketView(IsAdminMixin, View):
    def get(self, request):
        file_data = {"img": SimpleUploadedFile("test.jpg", b"file data")}
        form = UploadObjectBucketForm({}, file_data)
        return render(request, 'home/upload_obj_bucket.html', {'form':form})
    def post(self, request):
        form = UploadObjectBucketForm(request.POST, request.FILES)
        if form.is_valid():
            key = form.cleaned_data
            tasks.upload_object_task.delay(key)
            messages.success(request, 'uploaded successully', 'success')
            return redirect('home:bucket_home')
        else:
            messages.error(request, 'not uploaded successully', 'danger')
            return render(request, 'home/upload_obj_bucket.html', {'form':form})
        

class CommentAllView(View):

    def get(self,request,slug):
        product = Products.objects.get(slug=slug)
        comments = Comment.objects.filter(product=product)
        return render(request, 'home/product_details.html', {'comments':comments, 'product':product })
        

class CommentCreateView(View):
    def post(self,request, product_slug):
        comment_form = CommentForm(request.POST)
        product = Products.objects.get(slug=product_slug)
        if comment_form.is_valid():
           
            cd_comment = comment_form.cleaned_data
            new_comment = Comment.objects.create(user_comment=cd_comment['user_commnet'],
                                            score=cd_comment['score'], img=cd_comment['img']).save(commit=False)
            new_comment.user = request.user
            new_comment.product = product
            new_comment.save()
            
        else:
            messages.error(request,'please correct your anserwer', 'danger')

        return redirect('home:product_details', product.slug)
            






        





