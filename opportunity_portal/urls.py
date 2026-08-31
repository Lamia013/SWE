from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.job_list,
        name='job_list'
    ),


    path(
        'jobs/',
        views.job_list,
        name='job_list'
    ),

    path(
        'jobs/<int:job_id>/apply/',
        views.apply_job,
        name='apply_job'
    ),

    path(
        'jobs/<int:job_id>/bookmark/',
        views.bookmark_job,
        name='bookmark_job'
    ),

    path(
        'applicant-dashboard/',
        views.applicant_dashboard,
        name='applicant_dashboard'
    ),

    path(
        'organization-dashboard/',
        views.organization_dashboard,
        name='organization_dashboard'
    ),

    path(
    'dashboard/',
    views.dashboard_redirect,
    name='dashboard'
),

]