from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, render, reverse, redirect
from .models import Portfolio, Project, Employee, ProjectMember, Task, \
    AssignedTask, ProjectRisk, MemberAbility, Risk, Ability, PortfolioStrategy, \
    OrganizationStrategy, ProjectStrategy, Strategy
from django.contrib.auth import authenticate, login, logout
import datetime, decimal
from .forms import LoginForm, NewProjectForm, NewTaskForm, NewRiskForm, NewProjRiskForm, NewAbilityForm, \
    NewMemAbilityForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from .analytics import *
from  .analytic_settings import *
from collections import OrderedDict
from operator import itemgetter


@login_required
def index(request):
    context = {
        'latest_portfolio_list': Portfolio.objects.all(),
    }
    project_list = Project.objects.filter(portfolio_id__isnull=True)
    finished_projects = project_list.filter(state__in=['3', '5'])
    actual_projects = project_list.filter(state__in=['1', '2', '4'])
    project_count = actual_projects.count()
    finished_pr_count = finished_projects.count()
    employee_list = Employee.objects.all()
    employee_count = employee_list.count()
    my_projects = request.user.employee.projectmember_set.count()
    my_lead_projects= request.user.employee.project_set.count()
    my_tasks = request.user.employee.assignedtask_set.count()
    context['employee_list'] = employee_list
    context['employee_count'] = employee_count
    context['finished_projects'] = finished_projects
    context['actual_projects'] = actual_projects
    context['project_count'] = project_count
    context['finished_pr_count'] = finished_pr_count
    context['attractivness'] = ATTRACTIVNESS_POINT
    context['my_projects'] = my_projects
    context['my_lead_projects'] = my_lead_projects
    context['my_tasks'] = my_tasks


    return render(request, "dp/index.html", context)


@login_required
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    projects_count = portfolio.project_set.count
    return render(request, 'dp/portfolio_detail.html',
                  {'portfolio': portfolio, 'attractivness':ATTRACTIVNESS_POINT, 'max_attractivness':MAX_ATTRACTIVNESS, 'projects_count': projects_count,
                   'error_message': "You didn't select a choice."})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    members = ProjectMember.objects.filter(project_id=project_id)
    is_member = len(request.user.employee.projectmember_set.filter(project_id=project_id)) > 0
    finished_tasks = Task.objects.filter(in_project=project_id, state='3').all()
    actual_tasks = Task.objects.filter(in_project=project_id)
    actual_tasks = actual_tasks.filter(state__in=[1, 2, 4])
    risks_tmp = ProjectRisk.objects.filter(project_id=project_id)
    finished_risks = risks_tmp.filter(risk_state__in=[2, 3])
    actual_risks = risks_tmp.filter(risk_state__in=[0, 1])

    my_tasks = []
    for task in actual_tasks:
        task_info_tmp = {}
        task_info_tmp["obj"] = task
        task_info_tmp["isEditable"] = len(task.assignedtask_set.filter(employee_id=request.user.employee.id).all()) > 0
        my_tasks.append(task_info_tmp)

    actual_risk_count = actual_risks.count()
    finished_risks_count = finished_risks.count()
    actual_tasks_count = actual_tasks.count()
    finished_tasks_count = finished_tasks.count()
    member_count = members.count()

    useable_budget = None
    if project.plan_budget is not None:
        useable_budget = project.plan_budget - project.used_budget

    return render(request, 'dp/project_detail.html',
                  {'project': project, 'is_member': is_member,'attractivness':ATTRACTIVNESS_POINT, 'max_attractivness':MAX_ATTRACTIVNESS,
                   'useable_budget': useable_budget,
                   'finished_tasks': finished_tasks, 'finished_risks': finished_risks, 'actual_risks': actual_risks,
                   'actual_risk_count': actual_risk_count, 'finished_risks_count': finished_risks_count,
                   'actual_tasks_count': actual_tasks_count,
                   'finished_tasks_count': finished_tasks_count, 'my_tasks':my_tasks, 'member_count': member_count, })


@login_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    abilities = MemberAbility.objects.filter(member_id=employee_id)
    ability_count = abilities.count()
    proj_count = employee.projectmember_set.count()
    task_count = employee.assignedtask_set.count()
    return render(request, 'dp/employee_detail.html',
                  {'employee': employee, 'ability_count': ability_count, 'proj_count': proj_count,
                   'task_count': task_count, 'error_message': "You didn't select a choice."})


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
            else:
                form.add_error(None, "Username or password is incorrect!")
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
    if not request.user.is_superuser:
        return redirect(reverse('dp:index'))
    employees = Employee.objects.exclude(position="Administrator")
    employees = [(empl.id, empl.user.last_name+" "+ empl.user.first_name) for empl in employees]
    key_words = Strategy.objects.all()
    key_words = [(key_w.id, key_w.name) for key_w in key_words]
    if request.method == 'POST':
        form = NewProjectForm(request.POST, employee_list=employees, key_word_list=key_words)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            plan_budget = form.cleaned_data['plan_budget']
            project_manager = form.cleaned_data['project_manager']
            project_manager = Employee.objects.get(id=int(project_manager))
            type = form.cleaned_data['type']
            complexity = form.cleaned_data['complexity']
            urgency = form.cleaned_data['urgency']
            importance = form.cleaned_data['importance']
            strat = form.cleaned_data['key_words']
            members = form.cleaned_data['members']
            project = Project.objects.create(project_name=name, description=description, complexity=complexity,
                                             type=type, plan_budget=plan_budget, project_manager=project_manager,
                                             urgency=urgency, importance=importance,
                                             pub_date=datetime.now())
            project.save()
            for strat_id in strat:
                strat_tmp = Strategy.objects.get(id=strat_id)
                proj_strategy = ProjectStrategy.objects.create(strategy=strat_tmp, project=project)
                proj_strategy.save()
            for member_id in members:
                member_tmp = Employee.objects.get(id=member_id)
                projmember = ProjectMember.objects.create(member=member_tmp, project=project)
                projmember.save()
            return redirect(reverse('dp:index'))
    else:
        form = NewProjectForm(employee_list=employees, key_word_list=key_words)
    return render(request, 'dp/new_project.html', {'form': form})


@login_required
def new_port_project_handler(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    if request.user.employee.id != portfolio.portfolio_manager_id and not request.user.is_superuser:
        return redirect(reverse('dp:index'))
    employees = Employee.objects.exclude(position="Administrator")
    employees = [(empl.id, empl.user.username) for empl in employees]
    key_words = Strategy.objects.all()
    key_words = [(key_w.id, key_w.name) for key_w in key_words]

    if request.method == 'POST':
        form = NewProjectForm(request.POST, employee_list=employees, key_word_list=key_words)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            complexity = form.cleaned_data['complexity']
            plan_budget = form.cleaned_data['plan_budget']
            type = form.cleaned_data['type']
            urgency = form.cleaned_data['urgency']
            importance = form.cleaned_data['importance']
            project_manager = form.cleaned_data['project_manager']
            strat = form.cleaned_data['key_words']
            members = form.cleaned_data['members']
            project_manager = Employee.objects.get(pk=int(project_manager))
            project = Project.objects.create(project_name=name, description=description, complexity=complexity,
                                             type=type, plan_budget=plan_budget, project_manager=project_manager,
                                             urgency=urgency, importance=importance, portfolio_id=portfolio_id,
                                             pub_date=datetime.now())
            project.save()
            for strat_id in strat:
                strat_tmp = Strategy.objects.get(id=strat_id)
                proj_strategy = ProjectStrategy.objects.create(strategy=strat_tmp, project=project)
                proj_strategy.save()
            for member_id in members:
                member_tmp = Employee.objects.get(id=member_id)
                projmember = ProjectMember.objects.create(member=member_tmp, project=project)
                projmember.save()
            return redirect(reverse('dp:portfolio_detail', kwargs={"portfolio_id": portfolio_id}))
    else:
        form = NewProjectForm(employee_list=employees, key_word_list=key_words)
    return render(request, 'dp/new_project.html', {'form': form, "portfolio_id": portfolio_id})


@login_required
def new_task_handler(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.portfolio is None:
        if project.project_manager is None:
            if not request.user.is_superuser and not (request.user.employee.position == 'manager'):
                return redirect(reverse('dp:project_detail', kwargs={"project_id": project_id}))
        else:
            if not request.user.is_superuser and not (request.user.employee.id == project.project_manager):
                return redirect(reverse('dp:project_detail', kwargs={"project_id": project_id}))
    else:
        if project.project_manager is None:
            if not request.user.is_superuser and not (
                    request.user.employee.id == project.portfolio.portfolio_manager.id):
                return redirect(reverse('dp:project_detail', kwargs={"project_id": project_id}))
        else:
            if not request.user.is_superuser and not (request.user.employee.id == project.project_manager) \
                    and not (request.user.employee.id == project.portfolio.portfolio_manager.id):
                return redirect(reverse('dp:project_detail', kwargs={"project_id": project_id}))

    employees = ProjectMember.objects.filter(project_id=project_id).all()
    employees = [(empl.member_id, empl.member.user.last_name) for empl in employees]
    if request.method == 'POST':

        form = NewTaskForm(request.POST, employee_list=employees)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            assign_to = form.cleaned_data["employee"]
            task = Task.objects.create(name=name, description=description, in_project=project)
            task.save()
            for employee_assign_id in assign_to:
                emp = Employee.objects.get(id=employee_assign_id)
                assigned_task = AssignedTask.objects.create(employee_id=emp.id, task=task)
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
        form = NewProjRiskForm(request.POST, available_risk_list=available_risk_list)
        if form.is_valid():
            risk = form.cleaned_data['risk']
            risk_id = int(risk)
            risk_state = form.cleaned_data['risk_state']
            risk_impact = form.cleaned_data['risk_impact']
            probability = form.cleaned_data['probability']
            projrisk = ProjectRisk.objects.create(risk_id=risk_id, risk_state=risk_state,
                                                  risk_impact=risk_impact, probability=probability,
                                                  project_id=project_id)
            projrisk.save()
            messages.success(request, 'Form submission successful')
            return redirect(reverse('dp:project_detail', kwargs={"project_id": project_id}))
    else:
        form = NewProjRiskForm(available_risk_list=available_risk_list)
    return render(request, 'dp/new_proj_risk.html',
                  {'project_id': project_id, 'form': form, "available_risk_list": available_risk_list})


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
    fields = ['progress', 'state', 'start_date', 'deadline', 'possible_income', 'used_budget', 'plan_budget', 'urgency',
              'importance', 'project_manager']
    template_name = "dp/project_update_form.html"


class PortfolioUpdateView(UpdateView):
    model = Portfolio
    fields = ['portfolio_name', 'description', 'portfolio_manager']
    template_name = "dp/portfolio_update_form.html"


class TaskUpdateView(UpdateView):
    model = Task
    fields = ['name', 'description', 'state', 'progress', 'deadline', 'start_date']
    template_name = "dp/task_update_form.html"


class ProjRiskUpdateView(UpdateView):
    model = ProjectRisk
    fields = ['risk_state', 'risk_impact', 'probability']
    template_name = "dp/projrisk_update_form.html"


class MemAbilityUpdateView(UpdateView):
    model = MemberAbility
    fields = ['ability', 'experience']
    template_name = "dp/ability_update_form.html"

class ProjMemberUpdateView(UpdateView):
    model = ProjectMember
    fields = ['position']
    template_name = "dp/projmember_update_form.html"
