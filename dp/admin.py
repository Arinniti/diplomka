from django.contrib import admin
from .models import Portfolio, Project, Employee, ProjectMember, Ability, MemberAbility, Task, AssignedTask, ProjectNotes, \
    TaskNotes, Costumer, ProjectRisk, Risk, PortfolioStrategy, ProjectStrategy, OrganizationStrategy
from django.shortcuts import reverse


# Register your models here.
admin.site.register(Employee)
admin.site.register(Portfolio)
admin.site.register(Project)
admin.site.register(ProjectRisk)
admin.site.register(ProjectMember)
admin.site.register(Ability)
admin.site.register(MemberAbility)
admin.site.register(Task)
admin.site.register(AssignedTask)
admin.site.register(Risk)

admin.site.register(PortfolioStrategy)
admin.site.register(ProjectStrategy)
admin.site.register(OrganizationStrategy)



admin.site.register(ProjectNotes)
admin.site.register(TaskNotes)
admin.site.register(Costumer)


admin.site.site_url = "../dp/"