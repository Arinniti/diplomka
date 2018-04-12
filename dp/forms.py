from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Your username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class NewProjectForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(max_length=200)
    RISK_VALUES = (
        ('0.25', 'Small'),
        ('0.50', 'Medium'),
        ('0.75', 'Large'),
    )
    risk = forms.ChoiceField(required=True, choices=RISK_VALUES, label="", initial='', widget=forms.Select())
