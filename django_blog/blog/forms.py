from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """Form for user registration, extending Django's UserCreationForm."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class CustomUserChangeForm(UserChangeForm):
    """Form for user profile editing, extending Django's UserChangeForm."""
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture')

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        if self.instance.userprofile:
            self.fields['bio'].initial = self.instance.userprofile.bio
            self.fields['profile_picture'].initial = self.instance.userprofile.profile_picture

    def save(self, commit=True):
        user = super().save(commit=commit)
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.bio = self.cleaned_data.get('bio')
        user_profile.profile_picture = self.cleaned_data.get('profile_picture')
        if commit:
            user_profile.save()
        return user