from django.shortcuts import render, redirect
from time import localtime, strftime
from django.utils import timezone

# Create your views here.
def index(request):


    if not 'all' in request.session:
        request.session['all'] = []

    return render(request, 'words_app/index.html')

def addSession(request):

    new_dict = {
        "word" : request.POST['word'],
        "color" : request.POST['color'],
        "font" : request.POST['big_font'],
        "time" : strftime("%I:%M %p %b %d %Y", localtime())
    }
 

    temp = request.session['all']
    temp.append(new_dict)
    request.session['all'] = temp

    print (request.POST)
    print (request.session['all'])
    return redirect('/')

def clear(request):
    request.session['all'] = []
    return redirect('/')