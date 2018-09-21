# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.contrib import messages
import re
import bcrypt
from django.shortcuts import render, redirect

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


def index(request):
    return render(request,'login_reg/index.html')

def register(request):
    if request.method == 'POST':
        error = False
        
        if len(request.POST['first_name']) < 1 or len(request.POST['last_name']) < 1 or len(request.POST['email']) < 1 or len(request.POST['password']) < 1 or len(request.POST['confirm_password']) < 1:
            messages.error(request, "All fields are required")
            error = True  
        
        if len(request.POST['first_name']) < 2:
            messages.error(request, "First name is too short")
            error = True

        if len(request.POST['last_name']) < 2:
            messages.error(request, "Last name is too short")
            error = True

        if not request.POST['first_name'].isalpha() or not request.POST['last_name'].isalpha():
            messages.error(request, "Names must only contain letters")
            error = True

        if not re.match(EMAIL_REGEX, request.POST['email']):
            messages.error(request, "Must use a valid email address")
            error = True

        if len(User.objects.filter(email=request.POST['email'])):
            messages.error(request, "Email is already in use")
            error = True

        if len(request.POST['password']) < 8:
            messages.error(request, "Password must be longer than 8 characters")
            error = True

        if request.POST['confirm_password'] != request.POST['password']:
            messages.error(request, "Passwords don't match")
            error = True

        if error == True:
            return redirect('/')
    
        else:     
            hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = hashed_password
            )
            
            request.session['user_id'] = new_user.id
            
            return redirect('/success')
        
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        error = False
        retrieved_user = User.objects.get(email=request.POST['email'])
        retrieved_password = retrieved_user.password
        print retrieved_password
        print request.POST['password']
        if not bcrypt.checkpw(request.POST['password'].encode(), retrieved_password.encode()):
                messages.error(request, 'email/password incorrect')
                error = True

        if error == True:
            return redirect('/')
        else:
            return redirect('/success')
    else:
        return redirect('/')


def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/') 
    the_user = User.objects.get(id=request.session['user_id'])
    return render(request, 'login_reg/success.html', {'user': the_user})



