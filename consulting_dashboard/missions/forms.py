from django import forms
from .models import Mission, Complaint

class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ['name', 'type', 'end_date', 'budget_per_day', 'solo']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description']
