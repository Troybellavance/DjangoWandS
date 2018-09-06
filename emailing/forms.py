from django import forms

from .models import EmailingPreferences

class EmailingPreferencesForm(forms.ModelForm):
    # subscribed = forms.BooleanField(label='Receive Product Information Emails?', required=False)
    class Meta:
        model = EmailingPreferences
        fields = ['subscribed']
