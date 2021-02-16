from django import forms

class AddPostForm(forms.Form):
    content = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={
        'id': 'add-content',
        'placeholder': 'Post here.',
        'rows': 4,
        'class': 'form-control'
    }))