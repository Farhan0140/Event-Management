from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import Custom_User

# Register your models here.


@admin.register(Custom_User)
class Custom_Admin( UserAdmin ):
    model = Custom_User
    fieldsets = (
        (None, {'fields': ('username', 'password') }),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'email', 'profile_img')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ("Important Date's", {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'password1', 'password2', 'phone', 'profile_img')
        })
    )

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active'
    )

    search_fields = (
        'username',
        'email',
        'phone',
        'first_name',
        'last_name'
    )