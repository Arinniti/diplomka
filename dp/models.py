from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    birthday = models.DateField()
    photo = models.FileField( blank=True, null=True)
    GENDER_VALUES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(max_length=6, choices=GENDER_VALUES)
    def __str__(self):
        return self.user.username

class Portfolio(models.Model):
    portfolio_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    portfolio_manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.portfolio_name


class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True)
    project_name = models.TextField()
    popis = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


    RISK_VALUES = (
        ('0.25', 'Small'),
        ('0.50', 'Medium'),
        ('0.75', 'Large'),
    )
    risk = models.CharField(max_length=4, choices=RISK_VALUES)
    project_manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.project_name

    @classmethod
    def create(cls, name, description, risk, portfolio_id):
        project = cls(project_name=name)
        project.popis = description
        project.risk = risk
        project.portfolio_id = portfolio_id
        return project

class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.project.project_name


class Ability(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class MemberAbility(models.Model):
    member = models.ForeignKey(Employee, on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    experience = models.FloatField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
     )
    def __str__(self):
        return self.member.user.last_name