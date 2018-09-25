from django.shortcuts import render, redirect

# Create your views here.

def index(request):

    if not 'count' in request.session:
        request.session['count'] = 0
        
    return render(request, 'survey_app/index.html')

def process(request):

    request.session['count'] += 1
    request.session['name'] = request.POST['name']
    request.session['location'] = request.POST['location']
    request.session['language'] = request.POST['fav_language']
    request.session['comment'] = request.POST['comment']
    

    return redirect('/result')

def result(request):

    context = {
        "name" : request.session['name'],
        "location" : request.session['location'],
        "language" : request.session['language'],
        "comment" : request.session['comment'],
        "count" : request.session['count']
    }

    return render(request, 'survey_app/result.html', context)