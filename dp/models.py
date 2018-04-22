from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import reverse


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    birthday = models.DateField()
    photo = models.FileField( blank=True, null=True)
    salary = models.DecimalField(max_digits =4, decimal_places=3, null=True)
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
    budget = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    used_budget = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    def __str__(self):
        return self.portfolio_name


class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True, blank=True)
    project_name = models.TextField()
    description = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    used_budget = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField('date of deadline', null=True, blank=True)


    PRIORITY_VALUES = (
        ('0.75', 'High '),
        ('0.50', 'Normal'),
        ('0.25', 'Low'),
    )

    urgency = models.CharField(max_length=4, choices=PRIORITY_VALUES, null=True)
    importance = models.CharField(max_length=4, choices=PRIORITY_VALUES, null=True)

    RISK_VALUES = (
        ('0.25', 'Small'),
        ('0.50', 'Medium'),
        ('0.75', 'Large'),
    )
    risk = models.CharField(max_length=4, choices=RISK_VALUES, null=True)

    STATE_VALUES = (
        ('1', 'Planned'),
        ('2', 'Ongoing'),
        ('3', 'Finished'),
        ('4', 'Interrupted'),
        ('5', 'Stopped')
    )

    state = models.CharField(max_length=1, choices=STATE_VALUES, null=True)
    project_manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.project_name

    @classmethod
    def create(cls, name, description, risk, portfolio_id):
        project = cls(project_name=name)
        project.description = description
        project.risk = risk
        project.portfolio_id = portfolio_id
        return project

    def get_absolute_url(self):
        return reverse('dp:project_detail', kwargs={'project_id': self.pk})


class ProjectMember(models.Model):
    class Meta:
        unique_together = (('project', 'member'),)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position = models.CharField(max_length=200, null=True)
    def __str__(self):
        return "%s in %s" % (self.member.user.username, self.project.project_name)


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
    experience = models.FloatField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
     )
    def __str__(self):
        return self.member.user.last_name

class Task(models.Model):
    in_project= models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=200, null=True)
    deadline = models.DateTimeField('date of deadline', null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)


    STATE_VALUES = (
        ('1', 'Planned'),
        ('2', 'Ongoing'),
        ('3', 'Finished'),
        ('4', 'Interrupted')
    )
    state = models.CharField(max_length=1, choices=STATE_VALUES, default=1)

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
