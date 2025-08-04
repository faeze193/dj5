from django import forms
from crispy_forms.helper import FormHelper

class CartAddForm(forms.Form):
    quantity = forms.IntegerField(max_value=9,min_value=1 ,label='تعداد')
    
    def __init__(self, *args, **kwargs):
        super(CartAddForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].label = ''


class CouponForm(forms.Form):
    code = forms.CharField(label='coupon')


