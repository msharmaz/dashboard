from django.shortcuts import render, redirect
from time import gmtime, strftime
import re
import random
import bcrypt
from django.contrib import messages
from dashboard import models
from dashboard.models import *


def index(request):
    # print "usr_cnt: " + str(request.session['usr_cnt'])
    # print "usr level: ", request.session['usr_level']
    return render(request, "dashboard/index.html")

def register(request):
    if request.method == 'POST':
        print
        " Post "
        #validate data
        print
        '---validate data ---'
        print
        request.POST ()

        errors = User.objects.validate(request.POST)

        print (errors)
        if (errors):
            print ("==== errror ")
            for error in errors:
                messages.error(request, errors[error])
            print( messages)
            return render(request, "dashboard/register.html")
        print( "===== no errors ===")
        
        print ("====  create user ====")
        # hash password)
        hashPWD = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt())

        # check to see if email has been used
        try:
            usr = User.objects.get(email=request.POST['email'])
        except Exception as e:
            print( e, str(type(e))
                   )            # no user in db, register user
            # set user level
            
            if 'usr_cnt' in request.session:
                print( request.session['usr_cnt'])
                level = 5
                request.session['usr_cnt'] += 1
                if request.POST['from'] == 'register':
                    request.session['usr_level'] = 5
            else:
                level = 9
                request.session['usr_level'] = 9
                request.session['usr_cnt'] = 1

            print ("--usr_cnt", request.session['usr_cnt'])
            print( "--usr_level", request.session['usr_level'])
            # create new user
            newUser = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], pwd = hashPWD, user_level=level)
            print( " newUser: ", newUser)
            request.session['user'] = newUser.first_name
            request.session['uid'] = newUser.id
            
            if request.session['usr_level'] == 9:
                return redirect ('/dashboard/admin')
            else:
                return redirect ('/dashboard')

        if (usr):
            messages.error(request, "Error: Email has previously used to register another user.  Please use another email.")
            return render(request, "dashboard/register.html")
        
        return redirect('/register')
    return render(request, "dashboard/register.html")

def signin(request):
    if request.method == 'POST':
        print "---sign in validate data ---"
        print request.POST
        errors = User.objects.validate(request.POST)
        print "-- error: ", errors
        if (errors):
            print "==== errror "
            for error in errors:
                messages.error(request, errors[error])
            print messages
            return redirect("/signin")
        print "===== no errors ==="

        try:
            usr = User.objects.get(email = request.POST['email'])
        except Exception as e:
            print e, str(type(e))
            messages.error(request, "Error: Invalid User")
            return render(request, "dashboard/signin.html")

        if (usr):
            print usr
            valid = bcrypt.checkpw(request.POST['pwd'].encode(), usr.pwd.encode())
            if (valid):
                print "password match"
                request.session['uid'] = usr.id
                request.session['user'] = usr.first_name
                request.session['usr_level'] = usr.user_level
                if 'usr_cnt' not in request.session:
                    request.session['usr_cnt'] = 1
                else:
                    request.session['usr_cnt'] += 1

                print "--usr_cnt", request.session['usr_cnt']
                print "--usr_level", request.session['usr_level']

                # redirect to appropriate dashboard
                if usr.user_level == 9:
                    return redirect ('/dashboard/admin')
                else:
                    return redirect ('/dashboard')
            else:
                messages.error(request, "Error: Invalid Password")
                return redirect('/signin')
                # return render(request, "dashboard/signin.html")
        return redirect('/signin')
    return render(request, "dashboard/signin.html")

def sucess(request):
    return render(request, "dashboard/index.html")

def new(request):
    return render(request, "dashboard/new.html")

def add(request):
    return render(request, "dashboard/new.html")

def adm_db(request):
    print( "===== Dashboard adm === ")
    context = {
        'users': User.objects.all()
    }

    print( "users: ", context['users'])
    print ("level: ", context['users'][0].user_level)
    return render(request, "dashboard/dashboard_adm.html", context)

def dashboard(request):
    print ("===== Dashboard === ")
    context = {
        'user': User.objects.all()
    }

    print ("users: ", context['users'])
    print ("level: ", context['users'][0].user_level)
    return render(request, "dashboard/dashboard.html", context)

def show(request, uid):
    # get user info
    usr = User.objects.get(id = uid)

    # get all message for user
    messages = usr.received_msgs.all()

    context = {
        'user': usr,
        'messages': messages,
    }
    return render(request, "dashboard/wall.html", context)

def adm_edit(request, uid):
    print "---Adm Edit---"
    user = User.objects.get(id=uid)
    level = {
        '9': 'admin',
        '5': 'normal',
    }
    print "level: ", level[str(user.user_level)]
    context = {
        'uid': uid,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'level': level[str(user.user_level)],
        'description': user.description,
    }
    return render(request, "dashboard/adm_edit.html", context)

def edit(request):
    user = User.objects.get(id=request.session['uid'])
    level = {
        '9': 'admin',
        '5': 'normal',
    }
    context = {
        'uid': request.session['uid'],
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'level': level[str(user.user_level)],
        'description': user.description,
    }
    return render(request, "dashboard/edit.html", context)

def destroy(request, uid):
    print "---destroy---"
    user = User.objects.get(id=uid)
    level = {
        '9': 'admin',
        '5': 'normal',
    }
    context = {
        'uid': uid,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'level': level[str(user.user_level)],
        'description': user.description,
    }
    return render(request, "dashboard/confirm_delete.html", context)

def delete(request, uid):
    print "---delete---"
    print request.POST
    if request.POST['subBtn'] != 'No':
        usr = User.objects.get(id=uid)
        usr.delete()
    return redirect ('/dashboard/admin')

def update_info(request):
    print "------update"
    print "post: ", request.POST
    # validate data
    errors = User.objects.validate(request.POST)
    if (errors):
        print "==== errror "
        for error in errors:
            messages.error(request, errors[error])
        print messages
        if request.POST['from'] == 'adm':
            reURL = "/users/edit/"+ str(request.POST['id'])
            return redirect(reURL)
        else:
            return redirect('/users/edit')
    print "===== no errors ==="

    usr = User.objects.get(id=request.POST['id'])
    print usr
    usr.first_name = request.POST['first_name']
    usr.last_name = request.POST['last_name']
    usr.email = request.POST['email']
    usr.user_level = request.POST['user_level']
    usr.save()

    if request.POST['from'] == 'adm':
        return redirect('/dashboard/admin')
    else:
        return redirect('/dashboard')

def update_pwd(request):
    print "------update pwd"
    # validate data
    errors = User.objects.validate(request.POST)
    if (errors):
        print "==== errror "
        for error in errors:
            messages.error(request, errors[error])
        print messages
        if request.POST['from'] == 'adm':
            reURL = "/users/edit/"+ str(request.POST['id'])
            return redirect(reURL)
        else:
            return redirect('/users/edit')
    print "===== no errors ==="

    usr = User.objects.get(id=request.POST['id'])
    print usr

    hashPWD = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt())

    usr.pwd = hashPWD
    usr.save()

    if request.POST['from'] == 'adm':
        return redirect('/dashboard/admin')
    else:
        return redirect('/dashboard')

def update_desc(request):
    print "------update pwd"
    # validate data
    errors = User.objects.validate(request.POST)
    if (errors):
        print "==== errror "
        for error in errors:
            messages.error(request, errors[error])
        print messages
        return redirect('/users/edit')
    print "===== no errors ==="

    usr = User.objects.get(id=request.POST['id'])
    print usr

    usr.description = request.POST['description']
    usr.save()

    return redirect('/dashboard')

def post_msg(request):
    print "------post msg"
    print "post: ", request.POST
    # validate data
    msg_pstr = User.objects.get(id=request.session['uid'])
    msg_rcvr = User.objects.get(id=request.POST['to_id'])
    print msg_pstr, msg_rcvr
    msg = Message.objects.create(message=request.POST['postmsg'], msg_poster=msg_pstr, msg_receiver=msg_rcvr)

    reURL = "/users/show/" + request.POST['to_id']
    return redirect(reURL)

def post_cmt(request):
    print "------post cmt"
    print "post: ", request.POST
    # validate data
    cmt_pstr = User.objects.get(id=request.session['uid'])
    cmt_rcvr = User.objects.get(id=request.POST['to_id'])
    cmt_msg = Message.objects.get(id = request.POST['msg_id'])

    print cmt_pstr, cmt_msg
    cmt = Comment.objects.create(comment=request.POST['postcmt'], cmt_poster=cmt_pstr, msg_id=cmt_msg)

    reURL = "/users/show/" + request.POST['to_id']
    return redirect(reURL)

def reset(request):
    request.session.clear()
    return render(request, "dashboard/index.html")
