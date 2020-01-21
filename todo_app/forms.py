from django import forms
from base_user.models import MyUser
from .models import File


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label="Şifrə", widget=forms.PasswordInput())
    password_confirm = forms.CharField(label="Şifrə2", widget=forms.PasswordInput())

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("The two password fields must match.")
        return password_confirm

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'first_name', 'last_name']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)


class AddFile(forms.ModelForm):
    class Meta:
        model = File
        fields = ['desc', 'name', 'img']

# class AccesFile(forms.ModelForm):
#     class Meta:
#         model=File
#         fields=['access']