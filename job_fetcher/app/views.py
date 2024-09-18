from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from .models import Job
from .src.job_manager import JobManager


def get_job_list(request):

    pass

def get_all_jobs(request):
    job_manager = JobManager()
    all_jobs = job_manager.get_all()
    return JsonResponse({"jobs": all_jobs})

def manual_update(request):
    job_manager = JobManager()
    message = job_manager.store_into_database()
    return HttpResponse(f"Manually found jobs and added to the db.\n{message}")

def get_recent_job(request):
    # 必传）category 还有 date，（选传）搜索company / title
    pass