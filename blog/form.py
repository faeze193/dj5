from django import forms
from .models import Blogs

class BlogForm(forms.ModelForm):
    stitle = forms.CharField(max_length=500,required=False)
    simg = forms.ImageField(required=False)
    sdescriptions = forms.TimeField(required=False)
    class Meta:
        model = Blogs
        fields = ('sender','title','img', 'descriptions')