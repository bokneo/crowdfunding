from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from .models import Project, Invest
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
'''def index(request):
    query = "SELECT * FROM projects_project ORDER BY created_at DESC"
    c = connection.cursor()
    c.execute(query)
    project = c.fetchall()
    #project_dict = {'projects': project}
    page = request.GET.get('page', 1)
    paginator = Paginator(project, 2)
    try:
        project = paginator.page(page)
    except PageNotAnInteger:
        project = paginator.page(1)
    except EmptyPage:
        project = paginator.page(paginator.num_pages)
    return render(request,'projects/index.html', {'projects': project})'''


def index(request):
    cat = request.GET.get('cat', '')
    if request.GET:
        cat = request.GET.get('cat', '')
    else:
        cat = "all"
    if cat == "all":
        query = "SELECT * FROM projects_project ORDER BY created_at DESC"
        c = connection.cursor()
        c.execute(query)
        project = c.fetchall()
    elif cat == "featured":
        query = "SELECT * FROM projects_project WHERE pledged >= amount ORDER BY created_at DESC"
        c = connection.cursor()
        c.execute(query)
        project = c.fetchall()
    else:
        query = "SELECT * FROM projects_project WHERE category = \'%s\' ORDER BY created_at DESC" % (
            cat)
        c = connection.cursor()
        c.execute(query)
        project = c.fetchall()
    query = """SELECT *
		        FROM projects_project AS pp
		        WHERE pp.name = (
		            SELECT pi.name
		            FROM projects_invest AS pi
		            WHERE EXTRACT(DAY FROM pi.ts) BETWEEN EXTRACT(DAY FROM CURRENT_TIMESTAMP) AND EXTRACT(DAY FROM CURRENT_TIMESTAMP)
		            AND EXTRACT(MONTH FROM pi.ts)=EXTRACT(MONTH FROM CURRENT_TIMESTAMP)
			        AND EXTRACT(YEAR FROM pi.ts)=EXTRACT(YEAR FROM CURRENT_TIMESTAMP)
		            GROUP BY pi.name, pi.amount
		            HAVING SUM(pi.amount) >= ALL(
		                SELECT SUM(pi.amount)
		                FROM projects_invest AS pi
		                WHERE EXTRACT(DAY FROM ts)=EXTRACT(DAY FROM CURRENT_TIMESTAMP)
		                AND EXTRACT(MONTH FROM ts)=EXTRACT(MONTH FROM CURRENT_TIMESTAMP)
		                GROUP BY pi.name, pi.amount
		            )
				LIMIT 1
		        )
			"""
    c = connection.cursor()
    c.execute(query)
    feature = c.fetchall()
    query = """SELECT *
                FROM projects_project AS pp, projects_invest AS pi
                WHERE pi.name = pp.name
                AND NOT EXISTS(
                        SELECT *
                        FROM projects_invest AS pi1
                        WHERE pi.ts < pi1.ts
                        
                )"""
    c = connection.cursor()
    c.execute(query)
    newest = c.fetchall()
    query = """SELECT *
                FROM projects_project AS pp
                WHERE pp.name = (
                    SELECT pi1.name
                    FROM projects_invest AS pi1
                    WHERE EXTRACT(DAY FROM pi1.ts) BETWEEN EXTRACT(DAY FROM CURRENT_TIMESTAMP) - 6 AND EXTRACT(DAY FROM CURRENT_TIMESTAMP)
                    GROUP BY pi1.name
                    HAVING COUNT(pi1.name) >= ALL(
                        SELECT COUNT(pi2.name)
                        FROM projects_invest AS pi2
                        WHERE EXTRACT(DAY FROM pi2.ts) BETWEEN EXTRACT(DAY FROM CURRENT_TIMESTAMP) - 6 AND EXTRACT(DAY FROM CURRENT_TIMESTAMP)
                        GROUP BY pi2.name
                        )
                LIMIT 1
                )"""
    c = connection.cursor()
    c.execute(query)
    Highest = c.fetchall()
    query = """SELECT *
                FROM projects_project AS pp
                WHERE NOT EXISTS(
                        SELECT *
                        FROM projects_project AS pp1
                        WHERE pp.pledged < pp1.pledged
                        )"""
    c = connection.cursor()
    c.execute(query)
    Mostfund = c.fetchall()
    page = request.GET.get('page', 1)
    paginator = Paginator(project, 2)
    try:
        project = paginator.page(page)
    except PageNotAnInteger:
        project = paginator.page(1)
    except EmptyPage:
        project = paginator.page(paginator.num_pages)
    return render(request, 'projects/index.html', {'projects': project, 'cat': cat, 'feature': feature, 'newest': newest, 'Highest': Highest, 'Mostfund': Mostfund})


'''def feature(request):
    query = """SELECT *
                FROM projects_project AS pp
                WHERE pp.name = (
                    SELECT pi.name
                    FROM projects_invest AS pi
                    WHERE EXTRACT(DAY FROM ts)=EXTRACT(DAY FROM CURRENT_TIMESTAMP)
                    AND EXTRACT(MONTH FROM ts)=EXTRACT(MONTH FROM CURRENT_TIMESTAMP)
                    GROUP BY pi.name, pi.amount
                    HAVING SUM(pi.amount) >= ALL(
                        SELECT SUM(pi.amount)
                        FROM projects_invest AS pi
                        WHERE EXTRACT(DAY FROM ts)=EXTRACT(DAY FROM CURRENT_TIMESTAMP)
                        AND EXTRACT(MONTH FROM ts)=EXTRACT(MONTH FROM CURRENT_TIMESTAMP)
                        GROUP BY pi.name, pi.amount
                    )
                ) """
    c = connection.cursor()
    c.execute(query)
    project = c.fetchall()
    #project_dict = {'projects': project}
    return render(request, 'projects/index.html', {'projects': project, 'cat': cat})'''


def result(request):
    search_string = request.GET.get('name', '')
    query = 'SELECT * FROM projects_project WHERE name ~* \'%s\' OR category ~* \'%s\'' % (
        search_string, search_string)
    c = connection.cursor()
    c.execute(query)
    results = c.fetchall()
    query = 'SELECT count(*) FROM projects_project WHERE name ~* \'%s\' OR category ~* \'%s\'' % (
        search_string, search_string)
    c = connection.cursor()
    c.execute(query)
    count = c.fetchall()
    result_dict = {'records': results, 'count': count}
    return render(request, 'projects/result.html', result_dict)


def autocomplete(request):
    if 'term' in request.GET:
        search_string = request.GET.get('term', '')
        query = 'SELECT * FROM projects_project WHERE (name ~* \'%s\' OR category ~* \'%s\')' % (
            search_string, search_string)
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
    query = "SELECT * FROM auth_user"
    c = connection.cursor()
    c.execute(query)
    users = c.fetchall()
    users_dict = {'users': users}
    if request.method == 'POST':
        name = request.POST['title']
        query = 'SELECT * FROM projects_project WHERE name = \'%s\'' % (name)
        c = connection.cursor()
        c.execute(query)
        results = c.fetchall()
        if len(results) > 0:
            return render(request, 'projects/create.html', {'error': 'Project name has already been taken'})
        else:
            if request.POST['title'] and request.POST['body'] and request.FILES.get('image', False) and request.POST['start'] and request.POST['end'] and request.POST['amount'] and request.POST['category']:
                project = Project()
                project.name = request.POST['title']
                project.description = request.POST['body']
                project.image = request.FILES['image']
                project.start = request.POST['start']
                project.end = request.POST['end']
                project.amount = request.POST['amount']
                project.category = request.POST['category']
                user = request.user
                if user.is_superuser:
                    username = request.POST['userid']
                    user = User.objects.get(id=username)
                    print(user)
                    project.username = user
                else:
                    project.username = request.user
                project.save()
                return redirect('index')

            else:
                return render(request, 'projects/create.html', {'error': "All fields are required"})
    else:
        return render(request, 'projects/create.html', users_dict)


def detail(request, projectName):
    query = "SELECT * FROM projects_project WHERE name = \'%s\'" % (
        projectName)
    c = connection.cursor()
    c.execute(query)
    project = c.fetchall()
    project_dict = {'projects': project}
    return render(request, 'projects/detail.html', project_dict)


def invest(request):
    project_name = request.POST.get('projectName', '')
    amount = request.POST.get('amount', '')
    username = request.user.id
    if amount is not None and amount != '':
        if (int(amount) > 0):
            query = """INSERT INTO projects_invest (amount, name, "user", ts) VALUES (\'%s\', \'%s\', \'%s\', CURRENT_TIMESTAMP)""" % (
                amount, project_name, username)
            c = connection.cursor()
            c.execute(query)
            query = "UPDATE projects_project SET pledged = (SELECT SUM(amount) FROM projects_invest WHERE name = \'%s\') WHERE name = \'%s\'" % (
                project_name, project_name)
            c = connection.cursor()
            c.execute(query)
            query = "SELECT * FROM projects_project WHERE name = \'%s\'" % (
                project_name)
            c = connection.cursor()
            c.execute(query)
            project = c.fetchall()
            project_dict = {'projects': project}
            return render(request, 'projects/invest.html', project_dict)
        else:
            query = "SELECT * FROM projects_project WHERE name = \'%s\'" % (
                project_name)
            c = connection.cursor()
            c.execute(query)
            project = c.fetchall()
            project_dict = {'projects': project,
                            'error': 'Please key in the correct amount'}
            return render(request, 'projects/invest.html', project_dict)
    else:
        query = "SELECT * FROM projects_project WHERE name = \'%s\'" % (
            project_name)
        c = connection.cursor()
        c.execute(query)
        project = c.fetchall()
        project_dict = {'projects': project,
                        'error': 'Please key in the correct amount'}
        return render(request, 'projects/invest.html', project_dict)
