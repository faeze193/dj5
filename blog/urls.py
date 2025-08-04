from django.urls import path, include,re_path
from . import views


app_name = 'blog'


urlpatterns = [
    path('', views.BlogView.as_view(), name='blog'),
    path('create/new/', views.BlogcreateView.as_view(), name='blog_create'),
    re_path(r'(?P<slug>[-\w]+)/', views.BlogDetailsView.as_view(), name='blog_details'),
    
    
]
