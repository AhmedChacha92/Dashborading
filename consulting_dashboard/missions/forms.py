from django import forms
from .models import Mission, Complaint, Consultant

class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ['name', 'type', 'end_date', 'budget_per_day', 'solo']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description']

class ConsultantCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Consultant
        fields = ['email', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        user = super(ConsultantCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

class AssignMissionForm(forms.Form):
    consultant = forms.ModelChoiceField(queryset=Consultant.objects.all())
    missions = forms.ModelMultipleChoiceField(queryset=Mission.objects.all(), widget=forms.CheckboxSelectMultiple)