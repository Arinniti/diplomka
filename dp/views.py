from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import get_object_or_404, render, reverse, redirect
from .models import Portfolio, Project, Employee, ProjectMember
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, NewProjectForm

class IndexView(generic.ListView):
    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Portfolio.objects.all()
    template_name = 'dp/index.html'
    context_object_name = 'latest_portfolio_list'


    def get_queryset(self):

        return Portfolio.objects.all()


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['employee_list'] = Employee.objects.all()
        return context


def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    return render(request, 'dp/portfolio_detail.html',
                  {'portfolio': portfolio, 'error_message': "You didn't select a choice."})



# response = "You're looking at the detail of Portfolio %s."
# return HttpResponse(response % portfolio_id)


def project_detail(request,portfolio_id, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'dp/project_detail.html',
                  {'project': project, 'error_message': "You didn't select a choice."})


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

def new_project_handler(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    if request.user.employee.id != portfolio.portfolio_manager_id and not request.user.is_superuser:
        return redirect("dp:portfolio_detail", portfolio_id)

    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            risk = form.cleaned_data['name']
            project = Project.objects.create(name, description, risk, portfolio_id)
            project.save()
            #redirect
    else:
        form = NewProjectForm()
    return render(request, 'dp/new_project.html', {'form': form, 'portfolio_id' : portfolio_id})