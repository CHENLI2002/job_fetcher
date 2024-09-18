# TODO add comments

from datetime import datetime

from django.core.exceptions import ValidationError

from .get_jobs import get_jobs
from ..models import Job
from ..utils.helper import turn_result_into_dict

class JobManager:
    def __init__(self):
        pass

    def get_all(self):
        all_jobs = Job.objects.all()

        return turn_result_into_dict(all_jobs)

    def search_for_jobs(self, date, title, company, category):
        if date == "all" and category == "all" and company == "none" and title == 'none':
            return self.get_all()

        # TODO finish this method



    def store_into_database(self):
        jobs = get_jobs()
        updated = 0
        added = 0
        for job in jobs:
            # the assumption here is that if both title and company matches, they are essentially the same job
            company = job['comp']
            title = job['title']

            query_result = Job.objects.filter(company=company).filter(title=title)


            if len(query_result) == 0:
                # there's no replicate
                if job['date'] == 'N/A':
                    job['date'] = None
                current_job = Job(title=job['title'], location=job['location'], date_posted=job['date'],
                                  type=job['type'], job_url=job['url'], field=job['field'], company=job['comp'],
                                  description=job['description'])
                current_job.save()
                added += 1
            else:
                if len(query_result) != 1:
                    raise ValidationError("There are two similar jobs exist in the db")

                prev_date = query_result.first().date_posted
                current_date = job['date']
                if job['date'] == 'N/A':
                    continue
                if str(current_date) > str(prev_date):
                    query_result.update(title=job['title'], location=job['location'], date_posted=job['date'],
                                        type=job['type'], job_url=job['url'], field=job['field'], company=job['comp'],
                                        description=job['description'])
                updated += 1
        return f"added {added} new jobs, and updated {updated} old jobs"


    def search_job(self, type):
        pass
