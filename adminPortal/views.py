from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
    query = '''SELECT * FROM auth_user AS a WHERE NOT EXISTS (SELECT * FROM projects_project AS p WHERE p.id = a.id)'''
    c = connection.cursor()
    c.execute(query)
    users = c.fetchall()
    query = '''SELECT * FROM auth_user AS a WHERE EXISTS (SELECT * FROM projects_project AS p WHERE p.id = a.id)'''
    c = connection.cursor()
    c.execute(query)
    users_withProj = c.fetchall()
    user_dict = {'records': users, 'withproj': users_withProj}
    return render(request, 'adminPortal/user.html', user_dict)


def deluser(request):
    if request.method == "POST":
        deleteId = request.POST.get('deleteid', None)
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
    return render(request, 'adminPortal/project.html', project_dict)


def delproject(request):
    if request.method == "POST":
        deletename = request.POST.get('deleteid', None)
        query = 'DELETE FROM projects_project WHERE name = \'%s\'' % (
            deletename)
        c = connection.cursor()
        c.execute(query)
        return redirect('projectPortal')


def editdetail(request, name):
    if request.method == "POST":
        projectName = request.POST.get('editid', None)
        query = "SELECT * FROM projects_project WHERE name = \'%s\'" % (
            projectName)
        c = connection.cursor()
        c.execute(query)
        project = c.fetchall()
        project_dict = {'projects': project}
        return render(request, 'adminPortal/edit.html', project_dict)


def userdetail(request):
    if request.method == "POST":
        userid = request.POST.get('editid', None)
        query = "SELECT * FROM auth_user WHERE id = \'%s\'" % (userid)
        c = connection.cursor()
        c.execute(query)
        user = c.fetchall()
        user_dict = {'useredit': user}
        return render(request, 'adminPortal/edituser.html', user_dict)

def investment(request):
    if request.method == "POST":
        userid = request.POST.get('editid', None)
        query = '''SELECT * FROM projects_invest WHERE "user" = \'%s\'''' % (userid)
        c = connection.cursor()
        c.execute(query)
        investment = c.fetchall()
        investment_dict = {'investment': investment}
        return render(request, 'adminPortal/investment.html', investment_dict)

def delinvest(request):
    if request.method == "POST":
        deleteid = request.POST.get('deleteid', None)
        query = 'DELETE FROM projects_invest WHERE id = \'%s\'' % (
            deleteid)
        c = connection.cursor()
        c.execute(query)
        return redirect('userPortal')

def editinvest(request):
    if request.method == "POST":
        editid = request.POST.get('editid', None)
        amount = request.POST.get('amount', None)
        query = 'UPDATE projects_invest SET amount = \'%s\' WHERE id = \'%s\'' % (amount, editid)
        c = connection.cursor()
        c.execute(query)
        return redirect('userPortal')

def edituser(request):
    if request.method == "POST":
        userid = request.POST.get('editname', None)
        firstname = request.POST.get('first_name', None)
        lastname = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        password1 = request.POST.get('password1', False)
        password2 = request.POST.get('password2', False)
        print(password1, password2)
        u = User.objects.get(pk=userid)
        user = request.user
        if not (password1 or password2):
            query = '''UPDATE auth_user SET first_name = \'%s\',
                        last_name = \'%s\', email = \'%s\' WHERE id = \'%s\'''' % (firstname, lastname, email, userid)
            c = connection.cursor()
            c.execute(query)
        else:
            if request.POST['password1'] == request.POST['password2']:
                u.set_password(password1)
                u.save()
                query = '''UPDATE auth_user SET first_name = \'%s\',
                        last_name = \'%s\', email = \'%s\' WHERE id = \'%s\'''' % (firstname, lastname, email, userid)
                c = connection.cursor()
                c.execute(query)
            else:
                return render(request, 'adminPortal/edituser.html', {'error': 'Password does not match'})
        if user.is_superuser:
            return redirect('userPortal')
        else:
            return redirect('index')


def editproject(request):
    if request.method == "POST":
        editname = request.POST.get('editname', None)
        description = request.POST['description']
        cat = request.POST.get('category', None)
        amount = request.POST.get('amount', None)
        if request.FILES:
            image = request.FILES['image']
            project = Project.objects.get(pk=editname)
            project.image = request.FILES['image']
            project.description = description
            project.save()
            query = '''UPDATE projects_project SET image = \'images/%s\', category = \'%s\', amount = \'%s\' WHERE name = \'%s\'''' % (
                image, cat, amount, editname)
        else:
            project = Project.objects.get(pk=editname)
            project.description = description
            project.save()
            query = '''UPDATE projects_project SET category = \'%s\', amount = \'%s\' WHERE name = \'%s\'''' % (
                cat, amount, editname)

        c = connection.cursor()
        c.execute(query)
        return redirect('projectPortal')


def profile(request):
    user = request.user.id
    query = "SELECT * FROM auth_user WHERE id = \'%s\'" % (user)
    c = connection.cursor()
    c.execute(query)
    user = c.fetchall()
    user_dict = {'useredit': user}
    return render(request, 'adminPortal/profile.html', user_dict)


