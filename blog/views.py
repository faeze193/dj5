from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Blogs
from .form import BlogForm
from django.utils.encoding import uri_to_iri




# Create your views here.
class BlogView(View):
    def get(self,request):
        blogs = Blogs.objects.all()
        return render(request, 'blog/blogs.html', {'blogs':blogs})
    
class BlogDetailsView(View):
    def get(self,request,slug):
        blog = get_object_or_404(Blogs,slug=slug)
        sub_blog = blog.sblog.all()
        return render(request, 'blog/blog_details.html',{'blog':blog,'sub_blog':sub_blog})
    
class BlogcreateView(View): 

    form_class = BlogForm

    def get(self,request):
        form = self.form_class
        return render(request, 'blog/blog_create.html',{'form':form})
    
    def post(self,request):
        pass