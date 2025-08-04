from django.contrib import admin
from .models import Category, Products, Comment, ProductColors
from .models import Advertisement
#from .models import PromoBanner
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    raw_id_fields=['sub_category',]
    list_display = ('name', 'sub_category', 'is_sub')


class CommentInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ('product',)

class ProductColorsInline(admin.TabularInline):
    model = ProductColors
    raw_id_fields = ('product',)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    raw_id_fields=['category',]
    list_display = ('name',)
    inlines = (CommentInline,ProductColorsInline)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','product','score','created')

@admin.register(ProductColors)
class ProductColorsAdmin(admin.ModelAdmin):
    list_display = ('product','color_name','color_piker',)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title',)


#admin.site.register(PromoBanner)