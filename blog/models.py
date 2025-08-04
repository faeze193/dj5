from django.db import models
from django_jalali.db import models as jmodels
from django.utils.text import slugify

# Create your models here.

class Blogs(models.Model):
    img = models.ImageField()
    title = models.CharField(max_length=5000)
    sender = models.CharField(max_length=100 ,default='faeze')
    slug = models.SlugField(allow_unicode=True,max_length=255)
    descriptions = models.TextField()
    created = jmodels.jDateTimeField(auto_now_add=True,)
    updated = jmodels.jDateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title,allow_unicode=True)
        super(Blogs, self).save(*args, **kwargs)
    class Meta:
        ordering = ('updated',)
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class SubBlogs(models.Model):
    blog = models.ForeignKey(Blogs,on_delete=models.CASCADE,related_name="sblog")
    img = models.ImageField(null=True,blank=True)
    title = models.CharField(max_length=5000,null=True,blank=True)
    descriptions = models.TextField(null=True,blank=True)