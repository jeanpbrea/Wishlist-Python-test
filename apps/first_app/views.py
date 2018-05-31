from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import User
from .models import Item
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'first_app/index.html')

def register(request):
    result = User.objects.reg_validator(request.POST)
    if 'errors' in result:
         for key, value in result['errors'].items():
             messages.error(request, value)
    else: messages.success(request, 'Congratulations you have Registered!')
    return redirect('/')

def login(request):
      if request.method == "POST":
        users_with_same_email = User.objects.filter(email = request.POST['email'])
        if len(users_with_same_email) > 0:
            print('user with this email exsists')
            the_user = users_with_same_email.first()
            if bcrypt.checkpw(request.POST['password'].encode('utf-8'), the_user.password.encode('utf-8')):
                request.session['user_id'] = the_user.id
                request.session['name'] = the_user.name
                messages.success(request, 'you have logged out,{}!'.format(request.session['name']))
                return redirect('/dashboard/')
            else:
                print('passwords do not match')
                messages.error(request, 'Your password is incorrect!')
                return redirect('/')
        else:
            messages.error(request, 'Please type in your login information')
            return redirect('/')

def dashboard(request):
    curr_items = Item.objects.all()
    my_wish = Item.objects.filter(wishers=request.session['user_id'])
    context ={
        'items' : curr_items,
        'my_wishes' : my_wish

    }
    return render(request, 'first_app/dashboard.html',context)

def addw(request, item_id):
        user = User.objects.get(id=request.session['user_id'])
        item = Item.objects.get(id=item_id)
        user.wish_items.add(item)
        user.save()
        return redirect('/dashboard')

def removew(request, item_id):
        user = User.objects.get(id=request.session['user_id'])
        item = Item.objects.get(id=item_id)
        user.wish_items.remove(item)
        return redirect('/dashboard/')


def create_show(request):
    return render(request, 'first_app/create.html')

def create(request):
    user = User.objects.get(id=request.session['user_id'])
    Item.objects.create(name = request.POST['item'], added_by=user)

    return redirect ('/dashboard')

def wish_items_show(request, item_id):
    curr_items = Item.objects.get(id=item_id)
    all_users_who_wish = User.objects.filter(wish_items=item_id)
    context = {
        'items': curr_items,
        'users': all_users_who_wish

    }

    return render(request, 'first_app/wish_items.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')