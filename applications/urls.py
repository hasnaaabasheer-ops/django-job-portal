from django.urls import path

from .views import (
    apply_job,
    seeker_dashboard,
    employer_applications,
    update_application_status,
)

urlpatterns = [

    path(
        'jobs/<int:pk>/apply/',
        apply_job,
        name='apply_job'
    ),

    path(
        'seeker/dashboard/',
        seeker_dashboard,
        name='seeker_dashboard'
    ),

    path(
        'employer/applications/',
        employer_applications,
        name='employer_applications'
    ),

    path(
        'employer/applications/<int:pk>/status/',
        update_application_status,
        name='update_application_status'
    ),

]

