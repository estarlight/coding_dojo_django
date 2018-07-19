from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'logreg_app/index.html')

def register(request, methods='POST'):

    request.session['error'] = False
    request.session['action'] = request.POST['action']

    if len(request.POST['first_name']) ==0:
        messages.error(request, 'First name is required!')
        request.session['error'] = True

    if len(request.POST['first_name']) >0 and len(request.POST['first_name' ]) <2:
        messages.error(request, "First name must be longer than 2 letters")
        request.session['error'] = True

    if len(request.POST['last_name']) ==0:
        messages.error(request, 'Last name is required!')
        request.session['error'] = True

    if len(request.POST['last_name']) >0 and len(request.POST['last_name' ]) <2:
        messages.error(request, 'Last name must be longer than 2 letters')
        request.session['error'] = True

    if not request.POST['first_name'].isalpha():
        messages.error(request, "First Name cannot contain numbers")
        request.session['error'] = True

    if not request.POST['last_name'].isalpha():
        messages.error(request, "Last Name cannot contain numbers")
        request.session['error'] = True
    
    if len(request.POST['password']) < 0:
        messages.error(request,'Password is required')
        request.session['error'] = True
    
    if len(request.POST['password']) >0 and len(request.POST['password']) <8:
        messages.error(request, 'Password must be longer than 8 characters')
        request.session['error'] = True
    
    if not request.POST['password'] == request.POST['password_confirm']:
        messages.error(request, 'Passwords do not match')
        request.session['error'] = True

    if request.session['error'] == True:
        return redirect('/')
    else:
        # print('hello')
        
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        correct_hashed_pw = hashed_pw.decode('utf-8')

        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=correct_hashed_pw)

        new_user.save()

        request.session['user_id'] = new_user.id

        # print (request.session['user_id'])
        # print (request.session['action'])

        # print (new_user)
        return redirect('/success')


def success(request):

    context= {
        "user": User.objects.get(id=request.session['user_id'])
        }

    if request.session['action'] == 'register':
        messages.success(request, "You have registered successfully!")
    if request.session['action'] == 'login':
        messages.success(request, "You have logged in successfully!")


    return render(request, 'logreg_app/success.html', context)

def login(request):

    request.session['action'] = request.POST['action']

    try:
        user = User.objects.get(email=request.POST['email'])
    except User.DoesNotExist:
        messages.error(request, 'Your email does not exists. Please register.')
        return redirect('/')
    
    request.session['user_id'] = user.id
    result = bcrypt.checkpw(request.POST['password'].encode(),user.password.encode())

    if result == False:
        messages.error(request, 'Email/Password does not match. Please try again.')
    else:
        return redirect(reverse('success'))

def delete_all(request):
    User.objects.all().delete()
    return redirect('/')


