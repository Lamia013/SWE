from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User

def index(request):
    return render(request, 'index.html')

def CRUD_application(request):
    return render(request, 'CRUD_application.html')

def CRUD_applicant(request):
    return render(request, 'CRUD_applicant.html')

def CRUD_org(request):
    return render(request, 'CRUD_org.html')

def CRUD_post(request):
    return render(request, 'CRUD_post.html')

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