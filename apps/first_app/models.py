from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class wishManager(models.Manager):
    def reg_validator(self,postData):
        print(postData)
        errors = {}
        if len(postData['name']) == 0:
            errors['name'] = 'Your name is required.'
        elif len(postData['name'])<4:
            errors['name'] = 'Name needs to be at least 4 characters long.'
        if len(postData['alias']) == 0:
            errors['alias'] = 'An alias is required.'
        if len(postData['email']) == 0:
            errors['email'] = 'An Email is required.'
        if len(postData['password']) == 0:
            errors['password'] = 'Please enter a password.'
        elif len(postData['password']) < 8:
            errors['password'] = 'Password needs to be at least 8 characters'
        if len(postData['confirm']) == 0:
            errors['confirm'] = 'Please make sure password matches'
        if len(postData['dob']) == 0:
            errors['dob'] = 'Date of birth is requierd'
        if len(errors):
            result = {
                'errors' : errors
            }
            return result
       
        else:
            hash_pw = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())
            reg = self.create(
                name = postData['name'], 
                alias = postData['alias'], 
                email = postData['email'],
                password = hash_pw.decode('utf-8'),
                dob = postData['dob']
                
            )
            result = {
                'the_reg' : reg
            }
        return result

    def log_validator(self,postData):
        print(postData)
        errors = {}
        if len(postData['email']) == 0:
            errors['email'] = 'An Email is required.'
        if len(postData['password']) == 0:
            errors['password'] = 'Please enter a password.'
        print(errors)
        if len(errors):
            result = {
                'errors' : errors
            }
            return result
        else:
            log = self.create(email = postData['email'], password = postData['password'])
            result = {
                'the_log' : log
            }
            return result

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    dob = models.DateField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = wishManager()

class Item(models.Model):
    name = models.CharField(max_length = 50)
    added_by = models.ForeignKey(User, related_name="items", on_delete = models.CASCADE)
    wishers = models.ManyToManyField(User, related_name="wish_items")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    