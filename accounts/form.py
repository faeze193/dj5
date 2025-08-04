from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from .models import User

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["phone","first_name","last_name","email" ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone","first_name","last_name","email", "password", "is_active", "is_admin"]



class UserLoginForm(forms.Form):
    phone = forms.CharField(max_length=11, label="شماره تلفن خود را وارد کنید.")
    password = forms.CharField(label=' پسورد خود را وارد کنید',widget=forms.PasswordInput)    


class UserRegisterPhoneForm(forms.Form):
    phone = forms.CharField(max_length=11,label="شماره تلفن خود را وارد کنید.")


class UserRegisterCodeForm(forms.Form):
    code = forms.IntegerField(max_value=9999, label="کد ارسال شده را وارد کنید")

class UserRegisterInfoForm(forms.ModelForm):
    password1 = forms.CharField(label='پسورد خود را وارد کنید', widget=forms.PasswordInput)
    password2 = forms.CharField(label='پسورد خود را تکرار کنید', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

