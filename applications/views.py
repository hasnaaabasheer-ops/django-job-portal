from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db import IntegrityError

from jobs.models import Job

from .models import Application
from .forms import ApplicationForm


@login_required
def apply_job(request, pk):

    # Only job seekers can apply
    if not request.user.is_seeker:
        raise PermissionDenied

    job = get_object_or_404(
        Job,
        pk=pk
    )

    today = timezone.localdate()

    # Job must be active
    if job.status != 'Active':
        return render(
            request,
            'applications/application_closed.html',
            {
                'job': job,
                'message': 'This job is no longer active.'
            }
        )

    # Deadline protection
    if job.deadline < today:
        return render(
            request,
            'applications/application_closed.html',
            {
                'job': job,
                'message': 'The application deadline has passed.'
            }
        )

    # Check duplicate application
    already_applied = Application.objects.filter(
        job=job,
        applicant=request.user
    ).exists()

    if already_applied:
        return render(
            request,
            'applications/already_applied.html',
            {
                'job': job
            }
        )

    if request.method == 'POST':

        form = ApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.job = job
            application.applicant = request.user

            try:

                application.save()

            except IntegrityError:

                return render(
                    request,
                    'applications/already_applied.html',
                    {
                        'job': job
                    }
                )

            return redirect(
                'seeker_dashboard'
            )

    else:

        form = ApplicationForm()

    return render(
        request,
        'applications/apply.html',
        {
            'form': form,
            'job': job
        }
    )

@login_required
def seeker_dashboard(request):

    if not request.user.is_seeker:
        raise PermissionDenied

    applications = Application.objects.filter(
        applicant=request.user
    ).select_related(
        'job'
    ).order_by(
        '-applied_at'
    )

    total_applications = applications.count()

    applied_count = applications.filter(
        status='Applied'
    ).count()

    shortlisted_count = applications.filter(
        status='Shortlisted'
    ).count()

    rejected_count = applications.filter(
        status='Rejected'
    ).count()

    context = {
        'applications': applications,
        'total_applications': total_applications,
        'applied_count': applied_count,
        'shortlisted_count': shortlisted_count,
        'rejected_count': rejected_count,
    }

    return render(
        request,
        'applications/seeker_dashboard.html',
        context
    )

@login_required
def employer_applications(request):

    if not request.user.is_employer:
        raise PermissionDenied

    applications = Application.objects.filter(
        job__employer=request.user
    ).select_related(
        'job',
        'applicant'
    ).order_by(
        '-applied_at'
    )

    return render(
        request,
        'applications/employer_applications.html',
        {
            'applications': applications
        }
    )

@login_required
def update_application_status(request, pk):

    if not request.user.is_employer:
        raise PermissionDenied

    application = get_object_or_404(
        Application,
        pk=pk
    )

    # Only the job owner can change status
    if application.job.employer != request.user:
        raise PermissionDenied

    if request.method == 'POST':

        status = request.POST.get(
            'status'
        )

        if status in [
            'Shortlisted',
            'Rejected',
        ]:

            application.status = status

            application.save(
                update_fields=['status']
            )

    return redirect(
        'employer_applications'
    )