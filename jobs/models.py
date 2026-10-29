from django.db import models
from django.conf import settings


class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Closed', 'Closed'),
    ]

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    title = models.CharField(
        max_length=150
    )

    company_name = models.CharField(
        max_length=150
    )

    description = models.TextField()

    location = models.CharField(
        max_length=100
    )

    job_type = models.CharField(
        max_length=30,
        choices=JOB_TYPE_CHOICES
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    skills = models.TextField()

    experience = models.PositiveIntegerField(
        default=0,
        help_text='Required experience in years'
    )

    deadline = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title