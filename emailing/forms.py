from django import forms

from .models import EmailingPreferences

class EmailingPreferencesForm(forms.Modelform):
    subscribed = forms.BooleanField(label='Receive Product Information Emails?')
    class Meta:
        model = EmailingPreferences
        fields = ['subscribed']
