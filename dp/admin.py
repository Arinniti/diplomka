from django.contrib import admin
from .models import Portfolio, Project, Employee, ProjectMember, Ability, MemberAbility, Task, AssignedTask
# Register your models here.

admin.site.register(Portfolio)
admin.site.register(Project)
admin.site.register(Employee)
admin.site.register(ProjectMember)
admin.site.register(Ability)
admin.site.register(MemberAbility)
admin.site.register(Task)
admin.site.register(AssignedTask)