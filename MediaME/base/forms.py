from django.contrib.auth.models import User
from base.models import Genre, Type, Media, Room, Message
from django import forms


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['media', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class SearchForm(forms.Form):
    q = forms.CharField(max_length=200, label='Search', required=False,
    widget=forms.TextInput(attrs={'class': 'q_p'}) )
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=False, label="Genre",
    widget=forms.Select(attrs={'class': 'genre_p'}) )
    media_type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False, label="Media Type",
    widget=forms.Select(attrs={'class': 'type_p'}) )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].empty_label = "Any Genre"
        self.fields['media_type'].empty_label = "Any Media Type"


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your message...'})
        }