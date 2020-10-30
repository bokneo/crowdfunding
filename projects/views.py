from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from .models import Project, Invest

# Create your views here.
def index(request):
    query = "SELECT * FROM projects_project"
    c = connection.cursor()
    c.execute(query)
    project = c.fetchall()
    project_dict = {'projects': project}
    return render(request,'projects/index.html', project_dict)

def result(request):
    search_string = request.GET.get('name','')
    query = 'SELECT * FROM projects_project WHERE name ~* \'%s\'' % (search_string)
    c = connection.cursor()
    c.execute(query)
    results = c.fetchall()
    query = 'SELECT count(*) FROM projects_project WHERE name ~* \'%s\'' % (search_string)
    c = connection.cursor()
    c.execute(query)
    count = c.fetchall()
    result_dict = {'records': results, 'count': count}
    return render(request, 'projects/result.html', result_dict)

def autocomplete(request):
    if 'term' in request.GET:
        search_string = request.GET.get('term','')
        query = 'SELECT * FROM projects_project WHERE name ~* \'%s\'' % (search_string)
        c = connection.cursor()
        c.execute(query)
        results = c.fetchall()
        result_dict = {'records': results}
        titles = []
        for projects in result_dict['records']:
            titles.append(projects[0])
        data = JsonResponse(titles, safe=False)
        return data
    else:
        data = 'fail'
    return render(data, 'projects/index.html')

@login_required(login_url="accounts/signup")

def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.FILES['image']:
            project = Project()
            project.name = request.POST['title']
            project.description = request.POST['body']
            project.image = request.FILES['image']
            project.start = request.POST['start']
            project.end = request.POST['end']
            project.pledged = request.POST['pledged']
            project.username = request.user
            project.save()
            return redirect('index')

        else:
            return render(request, 'projects/create.html', {'error': "All fields are required"})  
    else:
        return render(request, 'projects/create.html')

def detail(request, projectName):
    query = "SELECT * FROM projects_project WHERE name = \'%s\'" % (projectName)
    c = connection.cursor()
    c.execute(query)
    project = c.fetchall()
    project_dict = {'projects': project}
    return render(request, 'projects/detail.html', project_dict)

def invest(request):
    project_name = request.POST.get('projectName', '')
    amount = request.POST.get('amount', '')
    username = request.user.id
    print(project_name, amount, username)
    query = """INSERT INTO projects_invest (amount, name, "user") VALUES (\'%s\', \'%s\', \'%s\')""" % (amount, project_name, username)
    c = connection.cursor()
    c.execute(query)
    query = "UPDATE projects_project SET amount = (SELECT SUM(amount) FROM projects_invest WHERE name = \'%s\') WHERE name = \'%s\'" % (project_name, project_name)
    c = connection.cursor()
    c.execute(query)
    return render(request, 'projects/detail.html')



