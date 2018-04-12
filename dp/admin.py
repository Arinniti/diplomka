from django.contrib import admin
from .models import Portfolio, Project, Employee, ProjectMember, Ability, MemberAbility
# Register your models here.

admin.site.register(Portfolio)
admin.site.register(Project)
admin.site.register(Employee)
admin.site.register(ProjectMember)
admin.site.register(Ability)
admin.site.register(MemberAbility)