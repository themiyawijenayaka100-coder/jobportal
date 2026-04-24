from django import forms

from .models import Job, Story


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "company", "description"]


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Story title"}),
            "content": forms.Textarea(attrs={"rows": 10, "placeholder": "Write your story..."}),
        }
