from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User, Organization
from opportunity_portal.models import Job
from accounts.models import Apply as Application
from django.contrib import messages


def index(request):
    return render(request, "index.html")


def CRUD_application(request):
    return render(request, "CRUD_application.html")


def CRUD_applicant(request):
    return render(request, "CRUD_applicant.html")


def add_page(request):
    return render(request, "add.html")


# =========================================================
# STUDENT CRUD
# =========================================================

@login_required
def student_list(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    students = User.objects.filter(
        role=User.Role.STUDENT
    ).order_by("id")

    return render(
        request,
        "student_list.html",
        {
            "students": students
        }
    )


@login_required
def student_add(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=User.Role.STUDENT
        )

        return redirect("student_list")

    return render(
        request,
        "student_add.html"
    )


@login_required
def student_edit(request, pk):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    student = get_object_or_404(
        User,
        pk=pk,
        role=User.Role.STUDENT
    )

    if request.method == "POST":

        student.username = request.POST.get("username")
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.email = request.POST.get("email")

        password = request.POST.get("password")

        if password:
            student.set_password(password)

        student.save()

        return redirect("student_list")

    return render(
        request,
        "student_edit.html",
        {
            "student": student
        }
    )


@login_required
def student_delete(request, pk):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    student = get_object_or_404(
        User,
        pk=pk,
        role=User.Role.STUDENT
    )

    if request.method == "POST":
        student.delete()

    return redirect("student_list")


# =========================================================
# ORGANIZATION CRUD
# =========================================================
@login_required
def CRUD_org(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    organizations = Organization.objects.select_related(
        "user"
    ).order_by(
        "organization_id"
    )

    return render(
        request,
        "CRUD_org.html",
        {
            "organizations": organizations
        }
    )


@login_required
def organization_add(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        organization_name = request.POST.get("organization_name")
        website = request.POST.get("website")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=User.Role.COMPANY
        )

        Organization.objects.create(
            organization_name=organization_name,
            website=website,
            user=user
        )

        return redirect("CRUD_org")

    return render(
        request,
        "organization_add.html"
    )


@login_required
def organization_edit(request, pk):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    organization = get_object_or_404(
        Organization.objects.select_related("user"),
        pk=pk
    )

    user = organization.user

    if request.method == "POST":

        organization.organization_name = request.POST.get(
            "organization_name"
        )

        organization.website = request.POST.get(
            "website"
        )

        user.username = request.POST.get(
            "username"
        )

        user.email = request.POST.get(
            "email"
        )

        password = request.POST.get("password")

        if password:
            user.set_password(password)

        user.save()
        organization.save()

        return redirect("CRUD_org")

    return render(
        request,
        "organization_edit.html",
        {
            "organization": organization
        }
    )


@login_required
def organization_delete(request, pk):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    organization = get_object_or_404(
        Organization,
        pk=pk
    )

    if request.method == "POST":
        organization.delete()

    return redirect("CRUD_org")


# =========================================================
# POST / JOB CRUD
# =========================================================

@login_required
def CRUD_post(request):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    posts = Job.objects.all().order_by("-created_at")

    return render(
        request,
        "CRUD_post.html",
        {
            "posts": posts
        }
    )

@login_required
def post_add(request):

    # Only ADMIN and COMPANY can create posts
    if request.user.role not in [User.Role.ADMIN, User.Role.COMPANY]:
        return redirect("dashboard")

    # Get the organization of the logged-in company user
    organization = None

    if request.user.role == User.Role.COMPANY:
        organization = get_object_or_404(
            Organization,
            user=request.user
        )

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        location = request.POST.get("location")
        job_type = request.POST.get("job_type")
        salary = request.POST.get("salary")
        deadline = request.POST.get("deadline")

        # ADMIN can choose any organization
        if request.user.role == User.Role.ADMIN:
            organization_name = request.POST.get("organization")

        # COMPANY can ONLY post for itself
        else:
            organization_name = organization.organization_name

        Job.objects.create(
            title=title,
            organization=organization_name,
            description=description,
            location=location,
            job_type=job_type,
            salary=salary,
            deadline=deadline
        )

        # Return to the appropriate dashboard
        if request.user.role == User.Role.ADMIN:
            return redirect("post_list")

        return redirect("dashboard")

    return render(
        request,
        "post_add.html",
        {
            "job_types": Job.JOB_TYPE_CHOICES,
            "organization": organization,
            "is_admin": request.user.role == User.Role.ADMIN,
        }
    )



@login_required
def post_edit(request, pk):
    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    job = get_object_or_404(
        Job,
        pk=pk
    )

    if request.method == "POST":

        job.title = request.POST.get("title")
        job.organization = request.POST.get("organization")
        job.description = request.POST.get("description")
        job.location = request.POST.get("location")
        job.job_type = request.POST.get("job_type")
        job.salary = request.POST.get("salary")
        job.deadline = request.POST.get("deadline")

        job.save()

        return redirect("CRUD_post")

    return render(
        request,
        "post_edit.html",
        {
            "job": job,
            "job_types": Job.JOB_TYPE_CHOICES
        }
    )



@login_required
def post_delete(request, pk):

    if request.user.role != User.Role.ADMIN:
        return redirect("dashboard")

    post = get_object_or_404(
        Job,
        pk=pk
    )

    if request.method == "POST":
        post.delete()

    return redirect("CRUD_post")


@login_required
def update_application_status(request, application_id, status):

    application = get_object_or_404(
        Application,
        id=application_id
    )

    # Make sure this application belongs to a job
    # posted by the logged-in organization
    if application.job.organization != request.user.username:

        messages.error(
            request,
            'You do not have permission to update this application.'
        )

        return redirect('organization_dashboard')

    if request.method == 'POST':

        if status == 'accepted':

            application.status = 'accepted'

            application.save()

            messages.success(
                request,
                'Application accepted successfully.'
            )

        elif status == 'rejected':

            application.status = 'rejected'

            application.save()

            messages.success(
                request,
                'Application rejected successfully.'
            )

        else:

            messages.error(
                request,
                'Invalid application status.'
            )

    return redirect(
        'organization_dashboard'
    )