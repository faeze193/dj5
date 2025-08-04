from django.contrib import admin
from .models import Blogs,SubBlogs

# Register your models here.
class SubBlogsInline(admin.TabularInline):
    model = SubBlogs
@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title','updated', 'created',)
    prepopulated_fields = {"slug": ("title",)}
    inlines = (SubBlogsInline,)
    
    


@admin.register(SubBlogs)
class SubBlogsAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)
