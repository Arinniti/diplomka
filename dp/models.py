import decimal
from dp.choices import *

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import reverse
from .analytics import EVM, optimization

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    birthday = models.DateField()
    photo = models.FileField( blank=True, null=True)
    salary = models.DecimalField(max_digits =9, decimal_places=2, null=True)
    GENDER_VALUES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(max_length=6, choices=GENDER_VALUES)
    def __str__(self):
        return self.user.username

class Portfolio(models.Model):
    portfolio_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', editable=False)
    portfolio_manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.portfolio_name

    def get_absolute_url(self):
        return reverse('dp:portfolio_detail', kwargs={'portfolio_id': self.pk})

class Strategy(models.Model):
    name = models.CharField(max_length=50)



class PortfolioStrategy(models.Model):
    class Meta:
        unique_together = (('portfolio', 'strategy'),)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)

class OrganizationStrategy(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    def __str__(self):
        return self.strategy.name

class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True, blank=True)
    project_name = models.TextField()
    description = models.CharField(max_length=200)
    plan_budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    used_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    manhours = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    pub_date = models.DateTimeField (auto_now_add=True)
    start_date = models.DateField ('date of start', null=True, blank=True)
    deadline = models.DateField ('date of deadline', null=True, blank=True)
    possible_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    complexity = models.CharField(max_length=1, choices=COMPLEXITY_VALUES, null=True)
    type = models.CharField(max_length=1, choices=TYPE_VALUES, null=True)
    urgency = models.CharField(max_length=1, choices=PRIORITY_VALUES, null=True)
    importance = models.CharField(max_length=1, choices=PRIORITY_VALUES, null=True)

    STATE_VALUES = (
        ('1', 'Planned'),
        ('2', 'Ongoing'),
        ('3', 'Finished'),
        ('4', 'Interrupted'),
        ('5', 'Stopped'),
    )
    state = models.CharField(max_length=1, choices=STATE_VALUES, default=1)
    progress = models.DecimalField(max_digits=3, decimal_places=2, default=0,
                                   validators=[MaxValueValidator(1.00), MinValueValidator(0.00)])

    project_manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.project_name

    @classmethod
    def create(cls, name, description, complexity, type, urgency, importance, project_manager, portfolio_id):
        project = cls(project_name=name)
        project.description = description
        project.portfolio_id = portfolio_id
        project.complexity = complexity
        project.type = type
        project.urgency = urgency
        project.importance = importance
        project.project_manager = project_manager
        return project

    def get_absolute_url(self):
        return reverse('dp:project_detail', kwargs={'project_id': self.pk})

    def risk(self, zero_if_not_set=False):
        project_risk = 0
        for risk in self.projectrisk_set.all():
            if risk.risk_state == 0 or risk.risk_state == 1:
                project_risk += (decimal.Decimal(risk.probability) * decimal.Decimal(risk.risk_impact))
        project_risk_count = self.projectrisk_set.filter(risk_state__in=[0, 1])
        if project_risk != 0:
            project_risk = (round(project_risk / len(project_risk_count), 0))

        return project_risk

    def evm(self):
        return EVM.new_instance(self)

    def optimalization(self):
        return optimization(self, OrganizationStrategy.objects.all())

class ProjectStrategy(models.Model):
    class Meta:
        unique_together = (('project', 'strategy'),)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)

class ProjectMember(models.Model):
    class Meta:
        unique_together = (('project', 'member'),)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position = models.CharField(max_length=200, null=True)
    def __str__(self):
        return "%s in %s" % (self.member.user.username, self.project.project_name)
    def get_absolute_url(self):
        return reverse('dp:project_detail', kwargs={'project_id': self.project_id})

class Ability(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class MemberAbility(models.Model):
    class Meta:
        unique_together = (('member', 'ability'),)
    member = models.ForeignKey(Employee, on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    experience = models.IntegerField(choices=ABILITY_EXPERIENCE_VALUES, null=True)
    def __str__(self):
        return self.member.user.last_name

    def get_absolute_url(self):
        return reverse('dp:employee_detail', kwargs={'employee_id': self.member.id})

class Task(models.Model):
    in_project= models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=200, null=True)
    deadline = models.DateField('date of deadline', null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    STATE_VALUES = (
        ('1', 'Planned'),
        ('2', 'Ongoing'),
        ('3', 'Finished'),
        ('4', 'Interrupted')
    )
    state = models.CharField(max_length=1, choices=STATE_VALUES, default=1)
    progress = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MaxValueValidator(1.00), MinValueValidator(0.00)])

    @classmethod
    def create(cls, name, description, project_id):
        task = cls(in_project=project_id)
        task.description = description
        task.name = name
        return task

    def get_absolute_url(self):
        return reverse('dp:project_detail', kwargs={'project_id': self.in_project.id})


class AssignedTask(models.Model):
    class Meta:
        unique_together = (('employee', 'task'),)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    @classmethod
    def create(cls, assigned_to, task):
        assignTask = cls(assigned_to=assigned_to)
        assignTask.task = task
        return assignTask

class Costumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_costumer = True
    def __str__(self):
        return self.user.username

class TaskNotes(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(Employee, on_delete=models.CASCADE)
    note = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

class ProjectNotes(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(Employee, on_delete=models.CASCADE)
    note = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

class Risk (models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=200, null=True)
    consequence = models.CharField(max_length=200, null=True)

class ProjectRisk (models.Model):
    class Meta:
        unique_together = (('project', 'risk'),)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE)

    risk_state = models.IntegerField(choices=RISK_STATE_VALUES, default=1)
    risk_impact = models.IntegerField(choices=RISK_IMPACT_VALUES, null=True)
    probability = models.IntegerField(choices=RISK_PROBABILITY_VALUES, null=True)

    def get_absolute_url(self):
        return reverse('dp:project_detail', kwargs={'project_id': self.project.id})

    def get_risk_value(self):
        return self.probability * self.risk_impact
