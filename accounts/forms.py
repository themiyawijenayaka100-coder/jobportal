from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, DirectMessage


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username"]

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        if not username:
            raise forms.ValidationError("Username is required.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "bio",
            "skills",
            "experience",
            "education",
            "resume_link",
            "profile_picture",
            "cv_file",
        ]


class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = DirectMessage
        fields = ["subject", "body"]
        widgets = {
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "body": forms.Textarea(attrs={"rows": 6, "placeholder": "Write your message..."}),
        }
