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

class NewTaskForm(forms.Form):
    def __init__(self, *args, **kwargs):
        employee_list = kwargs.pop('employee_list')
        super(NewTaskForm, self).__init__(*args, **kwargs)
        self.fields["employee"] = forms.MultipleChoiceField(
            required=False,
            initial=True,
            widget=forms.CheckboxSelectMultiple(),
            choices=[] if employee_list is None else employee_list,
        )
        super(NewTaskForm, self).full_clean()
    name = forms.CharField()
    description = forms.CharField(max_length=200)

