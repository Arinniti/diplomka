from tokenize import blank_re

from django import forms
from dp.choices import *


class LoginForm(forms.Form):
    username = forms.CharField(label='Your username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class NewProjectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        employee_list = kwargs.pop('employee_list')
        key_word_list = kwargs.pop('key_word_list')
        super(NewProjectForm, self).__init__(*args, **kwargs)
        self.fields["project_manager"] = forms.ChoiceField(
            required=False,
            initial=True,
            widget=forms.Select(),
            choices=[] if employee_list is None else employee_list,
        )
        self.fields["key_words"] = forms.MultipleChoiceField(
            required=False,
            initial=True,
            widget=forms.CheckboxSelectMultiple(),
            choices=[] if key_word_list is None else key_word_list,
        )
        super(NewProjectForm, self).full_clean()
    name = forms.CharField()
    description = forms.CharField(max_length=200)
    plan_budget = forms.DecimalField(max_digits=15, decimal_places=2)
    type = forms.ChoiceField(choices=TYPE_VALUES)
    complexity = forms.ChoiceField(choices=COMPLEXITY_VALUES)
    urgency = forms.ChoiceField(choices=PRIORITY_VALUES)
    importance = forms.ChoiceField(choices=PRIORITY_VALUES)



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
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=200)


class NewRiskForm(forms.Form):
    name = forms.CharField(max_length=50)
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
    risk_impact = forms.ChoiceField(choices=RISK_IMPACT_VALUES)
    probability = forms.ChoiceField(choices=RISK_PROBABILITY_VALUES)

class NewAbilityForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=200)

class NewMemAbilityForm(forms.Form):
    def __init__(self, *args, **kwargs):
        available_ability_list = kwargs.pop('available_ability_list')
        super(NewMemAbilityForm, self).__init__(*args, **kwargs)
        self.fields["ability"] = forms.ChoiceField(
            required=True,
            initial=True,
            widget=forms.Select(),
            choices=[] if available_ability_list is None else available_ability_list,
        )
        super(NewMemAbilityForm, self).full_clean()
    experience = forms.ChoiceField(choices = ABILITY_EXPERIENCE_VALUES , required=True)
