from django.urls import path, include
from django.contrib import admin

from . import views


app_name = 'dp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('portfolio/<int:portfolio_id>', views.portfolio_detail, name='portfolio_detail'),
    path('portfolio/<int:portfolio_id>/project/<int:project_id>', views.project_detail, name='project_detail'),
    path('employee/<int:employee_id>', views.employee_detail, name='employee_detail'),
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_handler, name='logout'),
    path(r'admin/', admin.site.urls, name='admin_panel'),
    path('portfolio/<int:portfolio_id>/project/new',views.new_project_handler , name='new_project'),

]