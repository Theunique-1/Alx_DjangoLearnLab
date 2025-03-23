from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag

class TagWidget(forms.CheckboxSelectMultiple):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.choices = [(tag.id, tag.name) for tag in Tag.objects.all()]


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
        if hasattr(self.instance, 'bio'):
            self.fields['bio'].initial = self.instance.bio
        if hasattr(self.instance, 'profile_picture'):
            self.fields['profile_picture'].initial = self.instance.profile_picture

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.bio = self.cleaned_data.get('bio')
        user.profile_picture = self.cleaned_data.get('profile_picture')
        if commit:
            user.save()
        return user
    

class PostForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        choices=[],
        widget=TagWidget(),
        required=False,
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'published_date']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or len(content.strip()) < 10:  # Example: minimum 10 characters
            raise forms.ValidationError('Comment must be at least 5 characters long.')
        return content