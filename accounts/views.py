from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from opportunity_portal.models import Job
from .models import User, Organization
from .forms import (
    StudentRegistrationForm,
    CompanyRegistrationForm,
)
from accounts.models import Apply as Application

# =========================================================
# REGISTER CHOICE
# =========================================================

def register(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(
        request,
        "accounts/register.html"
    )


# =========================================================
# STUDENT REGISTRATION
# =========================================================

def student_register(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = StudentRegistrationForm(request.POST)

        if form.is_valid():

            # Save student
            user = form.save()

            # Automatically login after registration
            login(request, user)

            messages.success(
                request,
                f"Welcome {user.first_name or user.username}!"
            )

            # Go directly to student dashboard
            return redirect("student_dashboard")

    else:

        form = StudentRegistrationForm()

    return render(
        request,
        "accounts/register_student.html",
        {
            "form": form
        }
    )


# =========================================================
# COMPANY REGISTRATION
# =========================================================

def company_register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = CompanyRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            Organization.objects.create(
                organization_name=form.cleaned_data["organization_name"],
                website=form.cleaned_data["website"],
                user=user
            )

            login(request, user)

            messages.success(
                request,
                f"Welcome {user.username}!"
            )

            return redirect("company_dashboard")

    else:

        form = CompanyRegistrationForm()

    return render(
        request,
        "accounts/register_company.html",
        {
            "form": form
        }
    )
# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("dashboard")

    admin_login = request.GET.get("role") == "admin"


    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            # If this is the Admin Login page,
            # only an ADMIN user can log in
            if admin_login and user.role != User.Role.ADMIN:
                messages.error(
                    request,
                    "This account does not have administrator access."
                )
                return redirect("login")

            # Normal login
            # Create login session
            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            # Send user according to role
            return redirect("dashboard")

        # Wrong username/password
        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html",
        {
        "admin_login": admin_login
        }
    )


# =========================================================
# MAIN DASHBOARD REDIRECTION
# =========================================================

@login_required
def dashboard(request):

    # -----------------------------------------------------
    # STUDENT
    # -----------------------------------------------------

    if request.user.role == User.Role.STUDENT:

        return redirect("applicant_dashboard")


    # -----------------------------------------------------
    # COMPANY
    # -----------------------------------------------------

    elif request.user.role == User.Role.COMPANY:

        return redirect("company_dashboard")


    # -----------------------------------------------------
    # ADMIN
    # -----------------------------------------------------

    elif request.user.role == User.Role.ADMIN:

        return redirect("admin_dashboard")


    # -----------------------------------------------------
    # INVALID ROLE
    # -----------------------------------------------------

    else:

        logout(request)

        messages.error(
            request,
            "Invalid user role."
        )

        return redirect("login")

# =========================================================
# COMPANY DASHBOARD
# =========================================================

@login_required
def company_dashboard(request):

    if request.user.role != User.Role.COMPANY:

        messages.error(
            request,
            "You do not have permission to access the company dashboard."
        )

        return redirect("dashboard")

    # Get the organization belonging to this company account
    try:
        organization = request.user.organization
    except Organization.DoesNotExist:

        messages.error(
            request,
            "No organization profile is associated with this account."
        )

        return redirect("dashboard")

    # Get only jobs posted by this organization
    jobs = Job.objects.filter(
        organization=organization.organization_name
    ).order_by(
        "-created_at"
    )

    # Get applications for this organization's jobs
    applications = Application.objects.filter(
        job__in=jobs
    ).select_related(
        "job",
        "user"
    ).order_by(
        "-applied_date"
    )

    return render(
        request,
        "opportunity_portal/organization_dashboard.html",
        {
            "organization": organization,
            "jobs": jobs,
            "applications": applications,
        }
    )

# =========================================================
# ADMIN DASHBOARD
# =========================================================

@login_required
def admin_dashboard(request):

    # Only admins can access this page
    if request.user.role != User.Role.ADMIN:

        messages.error(
            request,
            "You do not have permission to access the admin dashboard."
        )

        return redirect("dashboard")

    return render(
        request,
        "accounts/admin_dashboard.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    # Destroy login session
    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    # After logout user MUST login again
    return redirect("login")

def home(request):
    return render(request, "accounts/home.html")