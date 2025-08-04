from django.db import models
from home.models import Products
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django_jalali.db import models as jmodels
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ouser')
    paid = models.BooleanField(default=False)
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated =jmodels.jDateTimeField(auto_now=True)
    discount = models.IntegerField(default=None, null=True, blank=True)

    class Meta:
        ordering = ('paid', '-updated')

    def __str__(self):
        return f'{self.user}-{str(self.id)}'
    
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount/100)*total
            return int(total - discount_price)
        return total
    
    
    

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f'{str(self.id)}'

    def get_cost(self):
        return self.price*self.quantity
    
class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(10),MaxValueValidator(90)])
    valid_from = jmodels.jDateTimeField()
    valid_to = jmodels.jDateTimeField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code


