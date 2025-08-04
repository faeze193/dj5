from django.db import models
from django.urls import reverse
from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from colorfield.fields import ColorField
from django_jalali.db import models as jmodels
import statistics
from django.utils.text import slugify
# Create your models here.



class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,
                                     related_name='subcategory', null=True, blank=True)
    is_sub  = models.BooleanField(default=False)
    name = models.CharField(max_length=55, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug,])
    

    


class Products(models.Model):
    category = models.ManyToManyField(Category, related_name='category')
    name = models.CharField(max_length=55)
    slug = models.SlugField(unique=True)
    img = models.ImageField()
    descriptions = models.TextField()
    avalible = models.BooleanField(default=True)
    price = models.IntegerField()
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_absolute_url(self):
        return reverse('home:product_details', args=[self.slug,])

    def __str__(self):
        return self.name
    
    def mean_score(self):
        
        data = [i.num() for i in self.cproduct.all()]
        data = [i for i in data if i is not None]
        data = (sum(data))/len(data)
        return data
        
            
            

class ProductColors(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product_colors',blank=True,default=None)
    color_name = models.CharField(max_length=90)
    color_piker = ColorField(default='#FFFFFF')
    number = models.IntegerField(default=1)
    
    
    
    

    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cuser')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='cproduct')
    user_comment = models.TextField()
    is_buyer = models.BooleanField(default=False)
    is_reply = models.BooleanField(default=False)
    created = jmodels.jDateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True)
    like = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislike = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
    score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5,"امتیاز شما باید بین 1 تا 5 باشد"),MinValueValidator(1,"امتیاز شما باید بین 1 تا 5 باشد")], null=True,blank=True)

    
    def num(self):
        if self.score:
            return self.score
        else:
            return 1
        


class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True, null=True)
    image = models.ImageField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Advertisements"


        
    


    
    


    


        
    
