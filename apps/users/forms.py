from django import forms
from django.contrib.auth.models import User
from .models import Profile
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'id': 'avatarInput', 'class': 'hidden'}),
            'gender': forms.Select(choices=Profile.GENDER_CHOICES, attrs={'class': 'form-input, gender-select'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-input'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-input'}),
        }

class EmailForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'New Email'}),
    )

    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        # Check if email is already in use by another user
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")

        return email
    
class ThemeForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'theme': forms.Select(choices=Profile.THEME_CHOICES, attrs={'class': 'theme-select'})
        }