from django.contrib import admin
from .models import Portfolio, Project, Employee, ProjectMember, Ability, MemberAbility, Task, AssignedTask, ProjectNotes, \
    TaskNotes, Costumer, ProjectState, TaskState, ProjectRisk, Risk

# Register your models here.
admin.site.register(Employee)
admin.site.register(Portfolio)
admin.site.register(Project)
admin.site.register(ProjectState)
admin.site.register(ProjectRisk)
admin.site.register(ProjectMember)
admin.site.register(Ability)
admin.site.register(MemberAbility)
admin.site.register(Task)
admin.site.register(TaskState)
admin.site.register(AssignedTask)
admin.site.register(Risk)




admin.site.register(ProjectNotes)
admin.site.register(TaskNotes)
admin.site.register(Costumer)