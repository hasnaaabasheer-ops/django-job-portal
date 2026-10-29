from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'company_name',
        'employer',
        'job_type',
        'salary',
        'deadline',
        'status',
        'created_at',
    )

    list_filter = (
        'job_type',
        'status',
        'location',
    )

    search_fields = (
        'title',
        'company_name',
        'skills',
        'location',
    )