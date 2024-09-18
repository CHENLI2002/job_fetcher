from django.shortcuts import render
# TODO add comments
# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from .models import Job
from .src.job_manager import JobManager
from .utils.helper import check_if_is_date


def get_job_list(request):

    pass

@require_http_methods(["GET"])
def get_all_jobs(request):
    job_manager = JobManager()
    all_jobs = job_manager.get_all()
    return JsonResponse({"jobs": all_jobs})

@require_http_methods(["POST"])
def manual_update(request):
    job_manager = JobManager()
    message = job_manager.store_into_database()
    return HttpResponse(f"Manually found jobs and added to the db.\n{message}")

@require_http_methods(["GET"])
def get_recent_job(request):
    # 必传）category 还有 date，（选传）搜索company / title
    # Assume we have parameter category, date, company, title
    category = request.Get.get("category", "all")
    comp = request.Get.get("company", 'none')
    date = request.Get.get("date", "all")
    title = request.Get.get("title", "none")

    if not check_if_is_date(str(date)):
        raise ValueError("The date parameter pass in is not in date format")

    category = "none" if category == "" else category
    comp = "all" if comp == "" else comp
    title = "none" if title == "" else title
    job_manager = JobManager()
    job_manager.search_for_jobs(date=date, company=comp, category=category, title=title)

    pass