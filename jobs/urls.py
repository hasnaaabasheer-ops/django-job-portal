from django.urls import path

from .views import (
    home,
    job_list,
    job_detail,
    employer_dashboard,
    job_create,
    job_edit,
    job_delete,
)


urlpatterns = [

    path(
        '',
        home,
        name='home'
    ),

    path(
        'jobs/',
        job_list,
        name='job_list'
    ),

    path(
        'jobs/<int:pk>/',
        job_detail,
        name='job_detail'
    ),

    path(
        'employer/dashboard/',
        employer_dashboard,
        name='employer_dashboard'
    ),

    path(
        'employer/jobs/create/',
        job_create,
        name='job_create'
    ),

    path(
        'employer/jobs/<int:pk>/edit/',
        job_edit,
        name='job_edit'
    ),

    path(
        'employer/jobs/<int:pk>/delete/',
        job_delete,
        name='job_delete'
    ),


]