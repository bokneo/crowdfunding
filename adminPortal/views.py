from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from projects.models import Project

# Create your views here.
def adminPortal(request):
    query = 'SELECT * FROM projects_project'
    c = connection.cursor()
    c.execute(query)
    results = c.fetchall()
    result_dict = {'records': results}
    return render(request, 'adminPortal/admin.html', result_dict)

def userPortal(request):
    query = '''SELECT * FROM auth_user AS a WHERE NOT a.is_superuser AND NOT EXISTS (SELECT * FROM projects_project AS p WHERE p.id = a.id)'''
    c = connection.cursor()
    c.execute(query)
    users = c.fetchall()
    user_dict = {'records': users}
    return render(request, 'adminPortal/user.html', user_dict)

def deluser(request):
    if request.method == "POST":
        deleteId = request.POST.get('deleteid', None)
        print(deleteId)
        query = 'DELETE FROM auth_user WHERE id = \'%s\'' % (deleteId)
        c = connection.cursor()
        c.execute(query)
        return redirect('userPortal')

def projectPortal(request):
    query = '''SELECT * FROM projects_project'''
    c = connection.cursor()
    c.execute(query)
    projects = c.fetchall()
    project_dict = {'records': projects}
    print(project_dict)
    return render(request, 'adminPortal/project.html', project_dict)

def delproject(request):
    if request.method == "POST":
        deletename = request.POST.get('deleteid', None)
        query = 'DELETE FROM projects_project WHERE name = \'%s\'' % (deletename)
        c = connection.cursor()
        c.execute(query)
        return redirect('projectPortal')

def editdetail(request, name):
    if request.method == "POST":
        projectName = request.POST.get('editid', None)
        query = "SELECT * FROM projects_project WHERE name = \'%s\'" % (projectName)
        c = connection.cursor()
        c.execute(query)
        project = c.fetchall()
        project_dict = {'projects': project}
        return render(request, 'adminPortal/edit.html', project_dict)

def editproject(request):
    if request.method == "POST":
        editname = request.POST.get('editname', None)
        description = request.POST.get('description', None)
        image = request.FILES['image']
        project = Project.objects.get(pk = editname)
        project.image = request.FILES['image']
        project.save()
        query = "UPDATE projects_project SET description = \'%s\', image = \'images/%s\' WHERE name = \'%s\'" % (description, image, editname)
        c = connection.cursor()
        c.execute(query)
        return redirect('projectPortal')