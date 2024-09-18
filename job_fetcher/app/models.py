from django.db import models


# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    date_posted = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=50)
    job_url = models.CharField(max_length=1000)
    field = models.CharField(max_length=100, default="N/A")
    company = models.CharField(max_length=150, default="N/A")
    description = models.TextField(default="N/A")

    def __str__(self):
        return f"{self.title} posted at {self.date_posted}"
