from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption", "image"]

        widgets = {
            "caption": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "What's on your mind?",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

        widgets = {
            "text": forms.TextInput(
                attrs={
                    "placeholder": "Write a comment...",
                }
            ),
        }