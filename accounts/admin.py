from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .form import UserChangeForm, UserCreationForm
from .models import User, Otp, Address
from home.models import Comment





class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    


    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["phone","first_name","last_name", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = (
        ('main', {"fields": ("phone", "password")}),
        ("Personal info", {"fields": ("first_name","last_name")}),
        ("Permissions", {"fields": ("is_admin", "is_active","is_superuser", "groups", "user_permissions")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone","first_name","last_name", "is_admin","email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["phone"]
    ordering = ["last_name"]
    filter_horizontal = ["groups", "user_permissions"]


    def get_form(self, request, obj = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form

    
    

@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('phone','code', 'created')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user','ostan', 'phone_number')






# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
