from django.shortcuts import render
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# Create your views here.

def signup(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password1'] and request.POST['first_name'] and request.POST['last_name'] and request.POST['email']:
            if request.POST['password1'] == request.POST['password2']:
                    user = request.POST['username']
                    query = 'SELECT * FROM auth_user WHERE username = \'%s\'' % (user)
                    c = connection.cursor()
                    c.execute(query)
                    results = c.fetchall()
                    if len(results) > 0:
                        return render(request, 'accounts/signup.html', {'error':'Username has already been taken'})
                    else:
                        user = User.objects.create_user(request.POST['username'], password = request.POST['password1'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'])
                        if request.user.is_authenticated:
                            return redirect('index')
                        else:
                            auth.login(request, user)
                            return redirect('index')
            else:
                return render(request, 'accounts/signup.html', {'error':'Password does not match'})
        else:
            return render(request, 'accounts/signup.html', {'error':'All fields is required'})
    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == "POST":
        user = auth.authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username / Password does not match'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('index')
'''
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
                user = request.POST['email']
                query = 'SELECT * FROM auth_user WHERE email = \'%s\'' % (user)
                c = connection.cursor()
                c.execute(query)
                results = c.fetchall()
                
                if len(results) > 0:
                    return render(request, 'accounts/signup.html', {'error':'Username has already been taken'})
                else:
                    firstName = request.POST['first_name']
                    lastName = request.POST['last_name']
                    user = request.POST['email']
                    password1 = request.POST['password1']
                    query = """INSERT INTO auth_user VALUES(\'%s\', \'%s\',\'%s\', \'%s\')""" % (firstName, lastName, password1, user)
                    c = connection.cursor()
                    c.execute(query)
                    auth.login(request, user)
                    return redirect('index')
        else:
            return render(request, 'accounts/signup.html', {'error':'Password does not match'})
    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        query = 'SELECT * FROM users WHERE email = \'%s\'' % (username)
        c = connection.cursor()
        c.execute(query)
        results = c.fetchall()
        if results[0][2] == password:
            #request.session['email'] = username
            return render(request, 'crowdfunding/index.html', {'status': 'Logged in'})
        else:
            return render(request, 'accounts/login.html', {'error': 'Username / Password does not match'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == "POST":
        return render(request, 'crowdfunding/index.html', {'status': False})
        '''