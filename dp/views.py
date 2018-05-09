from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, render, reverse, redirect
from .models import Portfolio, Project, Employee, ProjectMember, Task, \
    AssignedTask, ProjectRisk, MemberAbility, Risk, Ability, PortfolioStrategy, OrganizationStrategy, ProjectStrategy
from django.contrib.auth import authenticate, login, logout
import datetime, decimal
from .forms import LoginForm, NewProjectForm, NewTaskForm, NewRiskForm, NewProjRiskForm, NewAbilityForm, NewMemAbilityForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from .analytics import *
from collections import OrderedDict
from operator import itemgetter




class IndexView(generic.ListView):
    template_name = 'dp/index.html'
    context_object_name = 'latest_portfolio_list'

    def get_queryset(self):
        return Portfolio.objects.all()

    def get_context_data(self, **kwargs):
        project_list = Project.objects.filter(portfolio_id__isnull=True)
        context = super(IndexView, self).get_context_data(**kwargs)
        context['employee_list'] = Employee.objects.all()
        context['project_list'] = project_list
        return context

@login_required
def index(request):
    context = {
        'latest_portfolio_list': Portfolio.objects.all(),
    }
    project_list = Project.objects.filter(portfolio_id__isnull=True)
    project_count = project_list.count()
    context['employee_list'] = Employee.objects.all()
    context['project_list'] = project_list
    context['project_count'] = project_count

    return render(request, "dp/index.html", context)


@login_required
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    projects_count = portfolio.project_set.count
    return render(request, 'dp/portfolio_detail.html',
                  {'portfolio': portfolio, 'projects_count': projects_count,
                   'error_message': "You didn't select a choice."})



@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    is_member = len(request.user.employee.projectmember_set.filter(project_id=project_id)) > 0
    finished_tasks = Task.objects.filter(in_project=project_id, state='3').all()
    useable_budget = None
    if  project.plan_budget is not None:
        useable_budget = project.plan_budget - project.used_budget

    return render(request, 'dp/project_detail.html',
                  {'project': project, 'is_member': is_member, 'useable_budget': useable_budget,
                   'finished_tasks': finished_tasks,  'error_message': "You didn't select a choice."})


@login_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'dp/employee_detail.html',
                  {'employee': employee, 'error_message': "You didn't select a choice."})


def login_page(request):
    current_url = request.resolver_match.url_name
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dp:index"))

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect(reverse('dp:index'))
                # return HttpResponseRedirect(reverse("dp:employee_detail", kwargs={"employee_id": user.employee.id}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'dp/authentication.html', {'form': form})


@login_required
def logout_handler(request):
    logout(request)
    return HttpResponseRedirect(reverse("dp:login_page"))


@login_required
def new_project_handler(request):
    if not request.user.is_superuser or request.user.is_authenticated:
        return redirect(reverse('dp:index'))
    employees = Employee.objects.all()
    employees = [(empl.id, empl.user.username) for empl in employees]
    if request.method == 'POST':
        form = NewProjectForm(request.POST, employee_list = employees)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            plan_budget = form.cleaned_data['plan_budget']
            project_manager = form.cleaned_data['project_manager']
            type = form.cleaned_data['type']
            complexity = form.cleaned_data['complexity']
            urgency = form.cleaned_data['description']
            importance = form.cleaned_data['importance']
            project = Project.objects.create(project_name=name, description=description,
                                             plan_budget=plan_budget,
                                             project_manager=project_manager, complexity=complexity,
                                             urgency=urgency, importance=importance,type=type)
            project.save()
            return redirect(reverse('dp:index'))
    else:
        form = NewProjectForm(employee_list= employees)
    return render(request, 'dp/new_project.html', {'form': form})


@login_required
def new_port_project_handler(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    if request.user.employee.id != portfolio.portfolio_manager_id and not request.user.is_superuser:
        return redirect(reverse('dp:index'))
    employees = Employee.objects.all()
    employees = [(empl.id, empl.user.username) for empl in employees]

    if request.method == 'POST':
        form = NewProjectForm(request.POST, employee_list =employees)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            project = Project.objects.create(project_name=name, description=description,
                                             pub_date=datetime.datetime.now())
            project.save()
            return redirect(reverse('dp:portfolio_detail', kwargs={"portfolio_id": portfolio_id}))
    else:
        form = NewProjectForm(employee_list =employees )
    return render(request, 'dp/new_project.html', {'form': form, "portfolio_id": portfolio_id})


@login_required
def new_task_handler(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.project_manager is None:
        if not request.user.is_superuser and not (
                project.portfolio is None and request.user.employee.position == 'manager') and not (project.portfolio.portfolio_manager_id == request.user.employee.id):
            return redirect(reverse('dp:project_detail', kwargs={"project_id": project_id}))
    elif project.project_manager_id != request.user.employee.id and request.user.is_superuser and not (
                project.portfolio is None and request.user.employee.position == 'manager') and not (project.portfolio.portfolio_manager_id == request.user.employee.id):
        return redirect(reverse('dp:project_detail', kwargs={"project_id": project_id}))

    employees = ProjectMember.objects.filter(project_id=project_id).all()
    employees = [(empl.member_id, empl.member.user.username) for empl in employees]
    if request.method == 'POST':

        form = NewTaskForm(request.POST, employee_list=employees)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            assign_to = form.cleaned_data["employee"]
            task = Task.objects.create(name=name, description=description, in_project=project_id)
            task.save()
            for employee_assign_id in assign_to:
                emp = Employee.objects.get(id=employee_assign_id)
                assigned_task = AssignedTask.objects.create(assigned_to=emp, task=task)
                assigned_task.save()
            messages.success(request, 'Form submission successful')
            return redirect(reverse('dp:project_detail', kwargs={"project_id": project_id}))
    else:
        form = NewTaskForm(employee_list=employees)
    return render(request, 'dp/new_task.html', {'form': form, "project_id": project_id})




@login_required
def new_risk_handler(request, project_id):
    if request.method == 'POST':
        form = NewRiskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            consequence = form.cleaned_data["consequence"]
            risk = Risk.objects.create(name=name, description=description, consequence=consequence)
            risk.save()
            messages.success(request, 'Form submission successful')
            return redirect(reverse('dp:project_detail', kwargs={"project_id": project_id}))
    else:
        form = NewRiskForm()
    return render(request, 'dp/new_risk.html', {'project_id': project_id, 'form': form})

@login_required
def new_proj_risk_handler(request, project_id):

    available_risk_list = Risk.objects.exclude(projectrisk__project_id=project_id).all()
    available_risk_list = [(risk.id, risk.name) for risk in available_risk_list]

    if request.method == 'POST':
        form = NewProjRiskForm(request.POST, available_risk_list = available_risk_list)
        if form.is_valid():
            risk = form.cleaned_data['risk']
            risk_id = int(risk)
            risk_state = form.cleaned_data['risk_state']
            risk_impact = form.cleaned_data['risk_impact']
            probability = form.cleaned_data['probability']
            projrisk = ProjectRisk.objects.create(risk_id = risk_id, risk_state=risk_state,
                                                  risk_impact=risk_impact, probability=probability, project_id=project_id )
            projrisk.save()
            messages.success(request, 'Form submission successful')
            return redirect(reverse('dp:project_detail', kwargs={"project_id": project_id}))
    else:
        form = NewProjRiskForm(available_risk_list  = available_risk_list)
    return render(request, 'dp/new_proj_risk.html', {'project_id': project_id, 'form': form, "available_risk_list":available_risk_list})



@login_required
def new_ability_handler(request, employee_id):
    if request.method == 'POST':
        form = NewAbilityForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            ability = Ability.objects.create(name=name, description=description)
            ability.save()
            messages.success(request, 'Form submission successful')
            return redirect(reverse('dp:employee_detail', kwargs={"employee_id": employee_id}))
    else:
        form = NewAbilityForm()
    return render(request, 'dp/new_ability.html', {'employee_id': employee_id, 'form': form})

@login_required
def new_emp_ability_handler(request, employee_id):
    available_ability_list = Ability.objects.exclude(memberability__member_id=employee_id).all()
    available_ability_list = [(ability.id, ability.name) for ability in available_ability_list]

    if request.method == 'POST':
        form = NewMemAbilityForm(request.POST, available_ability_list=available_ability_list)
        if form.is_valid():
            ability = form.cleaned_data['ability']
            ability_id = int(ability)
            experience = form.cleaned_data['experience']
            mem_ability = MemberAbility.objects.create(ability_id=ability_id, experience=experience,
                                                  member_id=employee_id)
            mem_ability.save()
            messages.success(request, 'Form submission successful')
            return redirect(reverse('dp:employee_detail', kwargs={"employee_id": employee_id}))
    else:
        form = NewMemAbilityForm(available_ability_list=available_ability_list)
    return render(request, 'dp/new_mem_ability.html',
                  {'employee_id': employee_id, 'form': form, "available_ability_list": available_ability_list})


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['progress', 'state', 'start_date', 'used_budget', 'plan_budget', 'urgency', 'importance', 'project_manager']
    template_name = "dp/project_update_form.html"

class PortfolioUpdateView(UpdateView):
    model = Portfolio
    fields = ['portfolio_name', 'description', 'portfolio_manager']
    template_name = "dp/portfolio_update_form.html"

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['name', 'description', 'state', 'progress', 'deadline', 'final_manhours' ]
    template_name = "dp/task_update_form.html"

class ProjRiskUpdateView(UpdateView):
    model = ProjectRisk
    fields = ['risk_state', 'risk_impact', 'probability' ]
    template_name = "dp/projrisk_update_form.html"

class MemAbilityUpdateView(UpdateView):
    model = MemberAbility
    fields = ['ability', 'experience' ]
    template_name = "dp/ability_update_form.html"
