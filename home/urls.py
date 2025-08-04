from django.urls import path, include, re_path
from . import views

app_name = 'home'

bucket_url = [
    path('', views.BucketHomeView.as_view(), name='bucket_home'),
    path('delete_obj/<str:key>/', views.DeleteObjectBucketView.as_view(), name='delete_obj_bucket'),
    path('download_obj/<str:key>/', views.DownloadObjectBucketView.as_view(), name='download_obj_bucket'),
    path('upload_obj/', views.UploadObjectBucketView.as_view(), name='upload_obj_bucket'),

]
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<slug:slug>/', views.ProductDitailsView.as_view(), name='product_details'),
    path('category/<slug:category_slug>/', views.HomeView.as_view(), name='category_filter'),
    path('comment/create/<slug:product_slug>/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comments/all/<slug:product_slug>/', views.CommentAllView.as_view(), name='comments_all'),
    path('like_comment/<int:comment_id>/', views.LikeCommentView.as_view(), name='like_comment'),
    path('dislike_comment/<int:comment_id>/', views.DisLikeCommentView.as_view(), name='dislike_comment'),
    path('search/', views.ProductsSearchView.as_view(), name='product_search'),
    
    #path('category/<slug:category_slug>/<slug:sub_category_slug>', views.HomeView.as_view(), name='sub_category_filter'),
    path('bucket/', include(bucket_url)),
    
]
