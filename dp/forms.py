from tokenize import blank_re

from django import forms
from dp.choices import *

class LoginForm(forms.Form):
    username = forms.CharField(label='Your username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class NewProjectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        employee_list = kwargs.pop('employee_list')
        super(NewProjectForm, self).__init__(*args, **kwargs)
        self.fields["project_manager"] = forms.ChoiceField(
            required=False,
            initial=True,
            widget=forms.Select(),
            choices=[] if employee_list is None else employee_list,
        )
        super(NewProjectForm, self).full_clean()
    name = forms.CharField()
    description = forms.CharField(max_length=200)
    plan_budget = forms.DecimalField(max_digits=15, decimal_places=2)
    used_budget = forms.DecimalField(max_digits=15, decimal_places=2)



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


class NewRiskForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(max_length=200)
    consequence = forms.CharField(max_length=200)

class NewProjRiskForm(forms.Form):
    def __init__(self, *args, **kwargs):
        available_risk_list = kwargs.pop('available_risk_list')
        super(NewProjRiskForm, self).__init__(*args, **kwargs)
        self.fields["risk"] = forms.ChoiceField(
            required=False,
            initial=True,
            widget=forms.Select(),
            choices=[] if available_risk_list is None else available_risk_list,
        )
        super(NewProjRiskForm, self).full_clean()

    risk_state = forms.ChoiceField(choices = RISK_STATE_VALUES , required=True)
    risk_has_impact_on = forms.ChoiceField(choices=RISK_IMPACT_TYPE_VALUES)
    risk_impact = forms.ChoiceField(choices=RISK_IMPACT_VALUES)
    probability = forms.ChoiceField(choices=RISK_PROBABILITY_VALUES)