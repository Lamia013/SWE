from django.db import models

class Notification(models.Model):
    Id = models.AutoField(primary_key=True)
    Message = models.TextField()
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Email


class Job(models.Model):
    JobId = models.AutoField(primary_key=True)

    Title = models.CharField(max_length=255, null=True, blank=True)
    Vacancy = models.IntegerField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Qualification = models.TextField(null=True, blank=True)
    Experience = models.TextField(null=True, blank=True)
    Specialization = models.CharField(max_length=255, null=True, blank=True)

    LastDateToApply = models.DateTimeField(null=True, blank=True)
    Salary = models.FloatField(null=True, blank=True)

    JobType = models.CharField(max_length=100, default="")

    Organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="Jobs"
    )

    Address = models.CharField(max_length=255, null=True, blank=True)
    Country = models.CharField(max_length=100, null=True, blank=True)
    State = models.CharField(max_length=100, null=True, blank=True)

    CreateDate = models.DateTimeField(auto_now_add=True)

    Tags = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.Title or "Untitled Job"



class Apply(models.Model):
    Id = models.AutoField(primary_key=True)

    Job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="ApplyForms"
    )

    # Applicant information
    FullName = models.CharField(max_length=255, default="")
    Email = models.EmailField(max_length=255, default="")

    # Resume
    ResumeData = models.BinaryField(null=True, blank=True)
    ResumeFileName = models.CharField(max_length=255, default="")
    ResumePath = models.CharField(max_length=500, default="")

    # Cover Letter
    CoverLetterData = models.BinaryField(null=True, blank=True)
    CoverLetterFileName = models.CharField(max_length=255, default="")
    CoverLetterPath = models.CharField(max_length=500, default="")

    # Application status
    Status = models.CharField(max_length=50, default="Pending")

    AppliedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.FullName} - {self.Job.Title}"