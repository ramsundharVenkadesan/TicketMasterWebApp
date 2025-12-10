from django import forms
from .models import Event


class Search(forms.ModelForm):
    genre = forms.CharField(max_length=100, required=True,
                            widget=forms.TextInput(attrs={
                                'class':'form-control',
                                'placeholder':'Type to search by genre',
                                'list': 'datalistOptions'}))
    city = forms.CharField(max_length=100, required=True,
                           widget=forms.TextInput(attrs={
                               "class":"form-control",
                               "placeholder":"Type to search by city"
                           }),
                           error_messages={
                               "required": "Enter a city!"
                           })

    class Meta:
        model = Event
        fields = ['genre', 'city']


class Save(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {field: forms.HiddenInput() for field in fields}