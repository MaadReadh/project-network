from django import forms

from network.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            'content'
        ]

        labels = {
            "content": ""
        }

        widgets = {
          'content': forms.Textarea(attrs={'rows':3, 'placeholder': 'Post Something...'}),
        }