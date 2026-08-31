from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [

    # =====================================================
    # DJANGO ADMIN
    # =====================================================

    path(
        "admin/",
        admin.site.urls
    ),


    # =====================================================
    # MAIN / PUBLIC PAGES
    # =====================================================

    path(
        "index/",
        views.index,
        name="index"
    ),

    path(
        "",
        include("accounts.urls")
    ),
    path("", include("opportunity_portal.urls")),

    path(
        "add/",
        views.add_page,
        name="add_page"
    ),


    # =====================================================
    # ADMIN CRUD PAGES
    # =====================================================

    path(
        "CRUD_post/",
        views.CRUD_post,
        name="CRUD_post"
    ),

    path(
        "CRUD_applicant/",
        views.CRUD_applicant,
        name="CRUD_applicant"
    ),

    path(
        "CRUD_org/",
        views.CRUD_org,
        name="CRUD_org"
    ),

    path(
        "CRUD_application/",
        views.CRUD_application,
        name="CRUD_application"
    ),


    # =====================================================
    # STUDENT CRUD
    # =====================================================

    path(
        "admin-students/",
        views.student_list,
        name="student_list"
    ),

    path(
        "admin-students/add/",
        views.student_add,
        name="student_add"
    ),

    path(
        "admin-students/edit/<int:pk>/",
        views.student_edit,
        name="student_edit"
    ),

    path(
        "admin-students/delete/<int:pk>/",
        views.student_delete,
        name="student_delete"
    ),
]