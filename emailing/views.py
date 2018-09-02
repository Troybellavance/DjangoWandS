from django.shortcuts import render
from django.views.generic import UpdateView

from .forms import EmailingPreferencesForm
from .models import EmailingPreferences

class EmailingPreferencesUpdateView(UpdateView):
