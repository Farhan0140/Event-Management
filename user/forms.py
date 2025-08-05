from django import forms
from django.contrib.auth.models import Group
from app_admin.forms import For_Mixin
import re
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from user.models import Custom_User

User = get_user_model()


class Register_Form(For_Mixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Your Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean_password(self):
        user_password = self.cleaned_data.get('password')
        errors = []

        if len(user_password) < 8:
            errors.append("Password must contain at least 8 characters")
        if not re.search(r'\d', user_password):
            errors.append("Password must contain at least one digit")
        if not re.search(r'[a-z]', user_password):
            errors.append("Password must contain at least one lowercase letter")
        if not re.search(r'[A-Z]', user_password):
            errors.append("Password must contain at least one uppercase letter")
        if not re.search(r'\W', user_password):
            errors.append("Password must contain at least one special character (!@£$%^&*()_+=}{?:~[]])")
        if re.search(r'\s', user_password):
            errors.append("Password must not contain whitespace")

        if errors:
            raise forms.ValidationError(errors)
        
        return user_password
    
    def clean(self):
        cln_data = super().clean()
        password = cln_data.get('password')
        c_password = cln_data.get('confirm_password')

        if password != c_password:
            raise forms.ValidationError("Password Don't Match")
        
        return cln_data
    
    def clean_email(self):
        email_from_user = self.cleaned_data.get('email')
        email_from_db = User.objects.filter(email = email_from_user).exists()

        if email_from_db:
            raise forms.ValidationError("This email already exist chose another")
        
        return email_from_user


class sign_in_form(For_Mixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class create_group_form(For_Mixin, forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']

        widgets = {
            "permissions": forms.CheckboxSelectMultiple()
        }
    

class Update_Profile_Form( For_Mixin, forms.ModelForm ):
    class Meta:
        model = Custom_User
        fields = ['first_name', 'last_name', 'phone', 'profile_img']


class Change_Password_Form( For_Mixin, PasswordChangeForm ):
    pass


class Reset_Password_Form( For_Mixin, PasswordResetForm ):
    pass

class Reset_Password_Confirm_Form( For_Mixin, SetPasswordForm ):
    pass