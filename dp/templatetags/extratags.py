from django import template
from dp.models import User, Employee

register = template.Library()

@register.simple_tag(takes_context=True)
def add_admin_to_context(context):
    admin_info = {}
    admin = Employee.objects.get(position = 'Administrator')
    admin_info['id'] = admin.id
    admin_info['first_name'] = admin.user.first_name
    admin_info['last_name'] = admin.user.last_name
    admin_info['email'] = admin.user.email

    context.dicts[0]["admin_info"] = admin_info
    return ''

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def mul(value, arg):
    return value * arg

@register.filter
def divide(value, arg):
    return value / arg