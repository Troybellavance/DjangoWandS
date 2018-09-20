from django import forms

from .models import EmailingPreferences

class EmailingPreferencesForm(forms.ModelForm):
    class Meta:
        model = EmailingPreferences
        fields = ['subscribed']
