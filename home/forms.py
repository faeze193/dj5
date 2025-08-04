from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Comment, ProductColors
from django.core.exceptions import ValidationError
from colorfield.forms import ColorField



class UploadObjectBucketForm(forms.Form):
    img = forms.ImageField()

file_data = {"img": SimpleUploadedFile("test.jpg", b"file data")}
form = UploadObjectBucketForm({}, file_data)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user_comment','img','score'] 
        def clean_user_comment(self):
            score = self.cleaned_data['score']
            if 1 > float(score) > 5:
                raise ValidationError("امتیاز شما باید بین 1 تا 5 ستاره باشد")
            return score


class ProductColorForm(forms.Form):
    class Meta:
        model = ProductColors
        fields = ('color_piker',)

class SearchForm(forms.Form):
    q = forms.CharField(label="جستجو", max_length=100)
    