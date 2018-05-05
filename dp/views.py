from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, render, reverse, redirect
from .models import Portfolio, Project, Employee, ProjectMember, Task, AssignedTask, MemberAbility
from django.contrib.auth import authenticate, login, logout
import datetime, decimal
from .forms import LoginForm, NewProjectForm, NewTaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

RISK_APETTITE = 15

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


def index(request):
    context = {
        'latest_portfolio_list': Portfolio.objects.all(),
    }
    project_list = Project.objects.filter(portfolio_id__isnull=True)
    context['employee_list'] = Employee.objects.all()
    context['project_list'] = project_list

    return render(request, "dp/index.html", context)


@login_required
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    more_projects = portfolio.project_set.count
    return render(request, 'dp/portfolio_detail.html',
                  {'portfolio': portfolio, 'more_projects': more_projects,
                   'error_message': "You didn't select a choice."})


def calculate_project_risk(project_id):
    project = get_object_or_404(Project, pk=project_id)
    project_risk = 0
    for risk in project.projectrisk_set.all():
        project_risk += (decimal.Decimal(risk.probability) * decimal.Decimal(risk.risk_impact))
    project_risk = "Not set" if project_risk == 0 else project_risk / len(project.projectrisk_set.all())
    return project_risk

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    is_member = len(request.user.employee.projectmember_set.filter(project_id=project_id)) > 0
    # finished_tasks = Task.objects.get(in_project=project_id, state__in=['3', '4'])
    finished_tasks = Task.objects.filter(in_project=project_id, state='3').all()
    project_risk = calculate_project_risk(project_id)
    useable_budget = None
    if  project.plan_budget is not None:
        useable_budget = project.plan_budget - project.used_budget

    return render(request, 'dp/project_detail.html',
                  {'project': project, 'is_member': is_member, 'useable_budget': useable_budget,
                   'finished_tasks': finished_tasks, 'project_risk': project_risk, 'error_message': "You didn't select a choice."})


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

            project = Project.objects.create(project_name=name, description=description,
                                             plan_budget=plan_budget, project_manager=project_manager)
            project.save()
            # redirect
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
            # redirect
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
            task = Task.objects.create(name=name, description=description, in_project=project)
            task.save()
            for employee_assign_id in assign_to:
                emp = Employee.objects.get(id=employee_assign_id)
                assigned_task = AssignedTask.objects.create(assigned_to=emp, task=task)
                assigned_task.save()
            messages.success(request, 'Form submission successful')
            # redirect
    else:
        form = NewTaskForm(employee_list=employees)
    return render(request, 'dp/new_task.html', {'form': form, "project_id": project_id})


class ProjectUpdateView(UpdateView):
    model = Project
    if model.project_manager is None:
        fields = ['project_name',  'used_budget', 'plan_budget', 'urgency', 'project_manager']
    else:
        fields = ['project_name', 'used_budget', 'plan_budget', 'urgency' ]
    template_name = "dp/project_update_form.html"

class PortfolioUpdateView(UpdateView):
    model = Portfolio
    fields = ['portfolio_name', 'description']
    template_name = "dp/portfolio_update_form.html"


class TaskUpdateView(UpdateView):
    model = Task
    fields = ['name', 'description' ]
    template_name = "dp/task_update_form.html"
