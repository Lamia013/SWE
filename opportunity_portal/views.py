from .forms import (
    ApplicationForm
)
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from accounts.models import Apply as Application
from django.contrib.auth.decorators import login_required
from accounts.models import User, Apply
from django.contrib import messages

from django.db.models import Q

from .models import (
    Job,
    Bookmark,
    UserProfile
)

from .forms import ApplicationForm

def job_list(request):

    jobs = Job.objects.all().order_by(
        '-created_at'
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


    # SEARCH FILTER

    if search:

        jobs = jobs.filter(

            Q(title__icontains=search) |

            Q(organization__icontains=search) |

            Q(description__icontains=search)

        )


    # LOCATION FILTER

    if location:

        jobs = jobs.filter(
            location__icontains=location
        )


    # JOB TYPE FILTER

    if job_type:

        jobs = jobs.filter(
            job_type=job_type
        )


    # BOOKMARKED JOB IDS

    bookmarked_jobs = []

    if request.user.is_authenticated:

        bookmarked_jobs = list(
            Bookmark.objects.filter(
                user=request.user
            ).values_list(
                'job_id',
                flat=True
            )
        )


    return render(
        request,
        'opportunity_portal/job_list.html',
        {
            'jobs': jobs,
            'search': search,
            'location': location,
            'job_type': job_type,
            'bookmarked_jobs': bookmarked_jobs,
        }
    )


@login_required
def apply_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )


    # CHECK USER ROLE

    try:

        role = request.user.role

    except:

        messages.error(
            request,
            'Please create an applicant profile first.'
        )

        return redirect('job_list')


    if request.user.role != User.Role.STUDENT:

        messages.error(
            request,
            'Only applicants can apply for jobs.'
        )

        return redirect('job_list')


    # CHECK DUPLICATE APPLICATION

    already_applied = Application.objects.filter(
        job=job,
        user=request.user
    ).exists()


    if already_applied:

        messages.warning(
            request,
            'You have already applied for this job.'
        )

        return redirect(
            'applicant_dashboard'
        )


    if request.method == 'POST':

        form = ApplicationForm(
            request.POST,
            request.FILES
        )


        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.job = job

            application.user = request.user

            application.save()


            messages.success(
                request,
                'Your application has been submitted successfully!'
            )


            return redirect(
                'applicant_dashboard'
            )


    else:

        form = ApplicationForm()


    return render(
        request,
        'opportunity_portal/apply.html',
        {
            'form': form,
            'job': job
        }
    )


@login_required
def bookmark_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )


    bookmark = Bookmark.objects.filter(
        job=job,
        user=request.user
    ).first()


    if bookmark:

        bookmark.delete()

        messages.success(
            request,
            'Job removed from bookmarks.'
        )

    else:

        Bookmark.objects.create(
            job=job,
            user=request.user
        )

        messages.success(
            request,
            'Job bookmarked successfully! 🔖'
        )


    return redirect(
        'job_list'
    )


@login_required
def applicant_dashboard(request):

    try:
        role = request.user.role

        if role != User.Role.STUDENT:
            messages.error(
                request,
                "You do not have permission to access the student dashboard."
            )
            return redirect("dashboard")

    except Exception:
        messages.error(
            request,
            "Unable to verify your account role."
        )
        return redirect("dashboard")

    applications = Apply.objects.filter(
        user=request.user
    ).select_related(
        'job'
    ).order_by(
        '-applied_date'
    )

    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related(
        'job'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        "opportunity_portal/applicant_dashboard.html",
        {
            "applications": applications,
            "bookmarks": bookmarks
        }
    )


@login_required
def organization_dashboard(request):

    try:

        role = request.user.userprofile.role

    except:

        messages.error(
            request,
            'Please create an organization profile.'
        )

        return redirect('index')


    if role != 'organization':

        messages.error(
            request,
            'Organization dashboard only.'
        )

        return redirect('index')


    jobs = Job.objects.filter(
        organization=request.user.username
    ).order_by(
        '-created_at'
    )


    applications = Application.objects.filter(
        job__in=jobs
    ).select_related(
        'job',
        'applicant'
    ).order_by(
        '-applied_at'
    )


    return render(
        request,
        'opportunity_portal/organization_dashboard.html',
        {
            'jobs': jobs,
            'applications': applications
        }
    )
@login_required
def dashboard_redirect(request):

    try:

        role = request.user.userprofile.role

        if request.user.role != User.Role.STUDENT:

            return redirect(
                'applicant_dashboard'
            )

        elif role == 'organization':

            return redirect(
                'organization_dashboard'
            )

    except UserProfile.DoesNotExist:

        return redirect('index')

    return redirect('index')