from django import forms
from home.models import Products


ID_SESSION_CARTS = 'cart'

class Cart:

    def __init__(self, request):
        
        self.session = request.session
        cart = self.session.get(ID_SESSION_CARTS)
        if not cart:
            cart = self.session[ID_SESSION_CARTS] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum( item['quantity'] for item in self.cart.values())
    

    def add(self,product,quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0,'price':str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def total_price(self):
        return sum(int(item['price'])*item['quantity'] for item in self.cart.values())
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[ID_SESSION_CARTS]
        self.save()


        