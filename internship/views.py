from django.shortcuts import render, redirect, get_object_or_404

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