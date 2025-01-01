# expert_dashboard/urls.py
from django.urls import path
from .views import upload_job_post_csv

urlpatterns = [
    path('upload-job-post-csv/<int:job_post_id>/', upload_job_post_csv, name='upload-job-post-csv'),
]