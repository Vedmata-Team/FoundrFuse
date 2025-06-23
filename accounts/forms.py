from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    user_type = forms.ChoiceField(choices=Profile.USER_TYPES, required=True, help_text='Are you a founder or an investor?')
    profile_image = forms.ImageField(required=True, help_text='Upload Logo or Image.')
    country = forms.CharField(max_length=64, required=True)
    state = forms.CharField(max_length=64, required=True)
    city = forms.CharField(max_length=64, required=True)
    pincode = forms.CharField(max_length=16, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2',
            'user_type', 'profile_image', 'country', 'state', 'city', 'pincode'
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            # Get the profile that was created by signal
            profile = user.profile
            profile.user_type = self.cleaned_data['user_type']
            profile.country = self.cleaned_data['country']
            profile.state = self.cleaned_data['state']
            profile.city = self.cleaned_data['city']
            profile.pincode = self.cleaned_data['pincode']
            profile.save()
        return user

class ProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False, help_text='Upload Logo or Image.')

    class Meta:
        model = Profile
        fields = (
            'bio', 'company_name', 'industry', 'country', 'state', 'city', 'pincode',
            'linkedin_profile', 'website', 'looking_for', 'profile_image'
        )
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself or your company'}),
            'looking_for': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What kind of connections are you looking for?'}),
            'linkedin_profile': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/your-profile'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://your-website.com'})
        }

class WaitlistForm(forms.Form):
    email = forms.EmailField(
        max_length=254, 
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'})
    )
    user_type = forms.ChoiceField(
        choices=Profile.USER_TYPES, 
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    company_name = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your company name (optional)'})
    )
