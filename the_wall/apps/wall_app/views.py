from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'wall_app/index.html')

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
        
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        correct_hashed_pw = hashed_pw.decode('utf-8')

        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=correct_hashed_pw)
        new_user.save()

        request.session['user_id'] = new_user.id

        return redirect('/wall')

def login(request, methods='POST'):

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
        return redirect(reverse('wall'))


def wall(request):

    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')

    context= {
        "user": User.objects.get(id=request.session['user_id']),
        # "messages" : Message.objects.all().select_related('user').prefetch_related('message_comment', 'message_comment__user')
        "wall_messages": Message.objects.all(),
    }

    return render(request, 'wall_app/wall.html', context)

def post_comment(request, id, methods='POST'):

    try:
        message = Message.objects.get(id=id)
        
    except Message.DoesNotExist:
        messages.error(request, "This message does not exist.")

    Comment.objects.create(user=User.objects.get(id=request.session['user_id']), message=message, content=request.POST['comment'])
   

    return redirect ('/wall')

def post_message(request):
     
    Message.objects.create(user=User.objects.get(id=request.session['user_id']),content=request.POST['message'])

    return redirect('/wall')

def logoff(request):
    request.session.clear()
    return redirect ('/')

def delete(request, id):

    deleted_message = Message.objects.get(id=id)

    if deleted_message.user.id == request.session['user_id']:
        deleted_message.delete()
    
    else:
        messages.error(request, 'You do not have the authority to delete this message')
    
    return redirect('/wall')




