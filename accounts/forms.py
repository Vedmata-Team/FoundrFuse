from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    user_type = forms.ChoiceField(choices=Profile.USER_TYPES, required=True, help_text='Are you a founder or an investor?')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type']
            )
        
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'company_name', 'industry', 'location', 'linkedin_profile', 'website', 'looking_for')
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
