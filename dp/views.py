from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, render, reverse, redirect
from .models import Portfolio, Project, Employee, ProjectMember, Task, AssignedTask
from django.contrib.auth import authenticate, login, logout
import datetime
from .forms import LoginForm, NewProjectForm, NewTaskForm
from django.contrib import messages



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


def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    usable_budget = "No budget"
    if portfolio.budget is not None:
        usable_budget =  portfolio.budget - portfolio.used_budget
    return render(request, 'dp/portfolio_detail.html',
                  {'portfolio': portfolio, 'usable_budget':usable_budget, 'error_message': "You didn't select a choice."})

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    is_member = len(request.user.employee.projectmember_set.filter(project_id=project_id)) > 0
    #finished_tasks = Task.objects.get(in_project=project_id, state__in=['3', '4'])
    finished_tasks = Task.objects.filter(in_project=project_id, state='3').all()

    return render(request, 'dp/project_detail.html',
                  {'project': project, 'is_member': is_member, 'finished_tasks' : finished_tasks,  'error_message': "You didn't select a choice."})


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'dp/employee_detail.html',
                  {'employee': employee, 'error_message': "You didn't select a choice."})


def login_page(request):
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
                return HttpResponseRedirect(reverse("dp:employee_detail", kwargs={"employee_id": user.employee.id}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'dp/authentication.html', {'form': form})


def logout_handler(request):
    logout(request)
    return HttpResponseRedirect(reverse("dp:login_page"))


def new_project_handler(request):
    if not request.user.is_superuser:
        return redirect(reverse('dp:index'))

    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            risk = form.cleaned_data['name']
            project = Project.objects.create(name, description, risk)
            project.save()
            # redirect
    else:
        form = NewProjectForm()
    return render(request, 'dp/new_project.html', {'form': form})


def new_port_project_handler(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    if request.user.employee.id != portfolio.portfolio_manager_id and not request.user.is_superuser:
           return redirect(reverse('dp:index'))

    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            risk = form.cleaned_data['risk']
            project = Project.objects.create(project_name=name, description=description, risk=risk, pub_date=datetime.datetime.now())
            project.save()
            # redirect
    else:
        form = NewProjectForm()
    return render(request, 'dp/new_project.html', {'form': form, "portfolio_id": portfolio_id})

def new_task_handler(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not request.user.is_superuser and project.project_manager.id != request.user.employee.id:
        return redirect(reverse('dp:project_detail', kwargs={"project_id":project_id}))

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
    fields = ['state', 'used_budget', 'project_name']
    template_name = "dp/project_update_form.html"

class PortfolioUpdateView(UpdateView):
    model = Portfolio
    fields = ['portfolio_name', 'description', 'used_budget']
    template_name = "dp/portfolio_update_form.html"

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['name', 'description', 'state']
    template_name = "dp/task_update_form.html"




