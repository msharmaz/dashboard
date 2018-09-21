from __future__ import unicode_literals

from django.db import models

import re


class UserManager(models.Manager):
    def validate(request, postdata):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        if 'first_name' in postdata:
            if len(postdata['first_name']) < 2:
                errors['first_name_length'] = "Error: First Name cannot be empty or less than 2 characters"
            if not re.match('^[\w-]+$', postdata['first_name']):
                print ("err: " + postdata['first_name'])
                errors['first_name_char'] = "Error: First Name can only be alpha numeric characters"
        if 'last_name' in postdata:
            if len(postdata['last_name']) < 2:
                errors['last_name_length'] = "Error: Last Name cannot be empty or less than 2 characters"
            if not re.match('^[\w-]+$', postdata['last_name']):
                errors['last_name_char'] = "Error: Last Name can only be alpha numeric characters"
        if 'email' in postdata:
            if len(postdata['email']) == 0:
                 errors['email_length'] = "Error: Email cannot be empty"               
            if not EMAIL_REGEX.match(postdata['email']):
                errors['email'] = "Error: Email format is incorrect"
        if 'pwd' in postdata:
            if (len(postdata['pwd']) < 8):
                errors['password_length'] = "Error: Password has to be longer than 8 characters"
        if 'pwd2' in postdata:
            if postdata['pwd'] != postdata['pwd2']:
                errors['password_match'] = "Error: Password and confirm password must match"
        return errors


class UserLevel(models.Model):
    level = models.IntegerField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return " id: " + str(self.id) + " name: " + self.name + " level: " + str(self.level)


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    user_level = models.IntegerField()
    pwd = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __unicode__(self):
        return " id: " + str(self.id) + " Fname: " + self.first_name + " Lname: " + self.last_name + " User Level: " + str(self.user_level) + " Email: " + self.email + " Desc: " + self.description + " PWD: " + self.pwd


class Message(models.Model):
    message = models.CharField(max_length=255)
    msg_poster = models.ForeignKey(User, related_name="posted_msgs")
    msg_receiver = models.ForeignKey(User, related_name="received_msgs")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return " id: " + str(self.id) + " msg: " + self.message + " msg_by: " + str(self.msg_poster) + " msg_for: " + str(self.msg_receiver) 


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    msg_id = models.ForeignKey(Message, related_name="tiedto_cmts")
    cmt_poster = models.ForeignKey(User, related_name="posted_cmts")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return " id: " + str(self.id) + " comment: " + self.comment + " to message:" + str(self.msg_id) + " cmt_by: " + str(self.cmt_poster) 
