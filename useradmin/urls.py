from django.urls import path, include
from . import views

app_name = 'useradmin'


urlpatterns = [
    path('',views.UserAdminView.as_view(),name='useradmin'),
    path('manage/users/',views.ManageUserAdminView.as_view(),name='manage_users'),
    path('manage/users/remove/<int:user_id>/',views.ManageRemoveUserAdminView.as_view(),name='manage_remove_users'),
    path('manage/users/comments/<int:user_id>/',views.ManageCommentsUserAdminView.as_view(),name='manage_comments_users'),
    path('manage/users/comments/delete/<int:comment_id>/',views.ManageCommentsUserDeleteAdminView.as_view(),name='manage_comment_delete'),
    path('manage/orders/',views.ManageOrdersAdminView.as_view(),name='manage_orders'),
    path('manage/orders/details/<int:order_id>/',views.ManageOrderDetailsAdminView.as_view(),name='manage_orders_details'),
    path('manage/user/details/<int:user_id>/',views.ManageUserDetailsAdminView.as_view(),name='manage_user_details'),
    path('manage/products/',views.ManageProductsAdminView.as_view(),name='manage_products'),
    
]
