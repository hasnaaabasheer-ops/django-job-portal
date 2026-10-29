from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Job
from .forms import JobForm


def home(request):
    return render(
        request,
        'jobs/home.html'
    )


def job_list(request):

    jobs = Job.objects.filter(
        status='Active',
        deadline__gte=timezone.localdate()
    )

    search = request.GET.get(
        'search',
        ''
    )

    location = request.GET.get(
        'location',
        ''
    )

    job_type = request.GET.get(
        'job_type',
        ''
    )

    experience = request.GET.get(
        'experience',
        ''
    )

    sort = request.GET.get(
        'sort',
        '-created_at'
    )

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(skills__icontains=search)
        )

    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    if job_type:
        jobs = jobs.filter(
            job_type=job_type
        )

    if experience:
        try:
            experience_value = int(experience)

            jobs = jobs.filter(
                experience__lte=experience_value
            )

        except ValueError:
            pass

    if sort not in [
        '-created_at',
        'created_at',
        '-salary'
    ]:
        sort = '-created_at'

    jobs = jobs.order_by(sort)

    context = {
        'jobs': jobs,
        'search': search,
        'location': location,
        'selected_job_type': job_type,
        'selected_experience': experience,
        'selected_sort': sort,
        'job_types': Job.JOB_TYPE_CHOICES,
    }

    return render(
        request,
        'jobs/job_list.html',
        context
    )


def job_detail(request, pk):

    job = get_object_or_404(
        Job,
        pk=pk
    )

    today = timezone.localdate()

    return render(
        request,
        'jobs/job_detail.html',
        {
            'job': job,
            'today': today,
        }
    )

@login_required
def employer_dashboard(request):

    if not request.user.is_employer:
        raise PermissionDenied

    today = timezone.localdate()

    jobs = Job.objects.filter(
        employer=request.user
    )

    total_jobs = jobs.count()

    active_jobs = jobs.filter(
        status='Active',
        deadline__gte=today
    ).count()

    total_applications = (
        jobs.aggregate(
            total=Count('applications')
        )['total'] or 0
    )

    new_applications = (
        jobs.filter(
            applications__status='Applied'
        )
        .aggregate(
            total=Count('applications')
        )['total'] or 0
    )

    recent_jobs = jobs.order_by(
        '-created_at'
    )[:5]

    context = {
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'new_applications': new_applications,
        'recent_jobs': recent_jobs,
    }

    return render(
        request,
        'jobs/employer_dashboard.html',
        context
    )

@login_required
def job_create(request):

    if not request.user.is_employer:
        raise PermissionDenied

    if request.method == 'POST':

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(commit=False)

            job.employer = request.user

            job.save()

            return redirect(
                'employer_dashboard'
            )

    else:

        form = JobForm()

    return render(
        request,
        'jobs/job_form.html',
        {
            'form': form,
            'title': 'Post New Job'
        }
    )

@login_required
def job_edit(request, pk):

    if not request.user.is_employer:
        raise PermissionDenied

    job = get_object_or_404(
        Job,
        pk=pk
    )

    # Ownership protection
    if job.employer != request.user:
        raise PermissionDenied

    if request.method == 'POST':

        form = JobForm(
            request.POST,
            instance=job
        )

        if form.is_valid():

            form.save()

            return redirect(
                'employer_dashboard'
            )

    else:

        form = JobForm(
            instance=job
        )

    return render(
        request,
        'jobs/job_form.html',
        {
            'form': form,
            'title': 'Edit Job'
        }
    )


@login_required
def job_delete(request, pk):

    if not request.user.is_employer:
        raise PermissionDenied

    job = get_object_or_404(
        Job,
        pk=pk
    )

    # Ownership protection
    if job.employer != request.user:
        raise PermissionDenied

    if request.method == 'POST':

        job.delete()

        return redirect(
            'employer_dashboard'
        )

    return render(
        request,
        'jobs/job_confirm_delete.html',
        {
            'job': job
        }
    )