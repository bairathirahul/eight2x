"""
    Project: 82x
    Authors: Rahul Bairathi, Nipun Gupta, Rajendra Jadi
"""
import json
import math
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pymongo import MongoClient

from eight2x_app.models import Status
from eight2x_app.lib.summary import FrequencySummarizer


def index(request):
    """
    Index view controller
    :param request:
    :return:
    """
    # Redirect to dashboard of authenticated
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')


def register(request):
    # Execute register method
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
        else:
            errors = [error[1] for error in form.errors.items()]
            print(errors)
            return render(request, 'registration/register.html', {'form': form, 'errors': errors})
    else:
        form = UserCreationForm()
        for field in form.fields:
            form.fields[field].widget.attrs['class'] = 'form-control'
    
    return render(request, 'registration/register.html', {'form': form})


def dashboard(request):
    """
    Dashboard view controller
    :param request: Request object
    :return: Dashboard view
    """
    
    # Setup pymongo connection
    dbconfig = settings.DATABASES['default']
    client = MongoClient(dbconfig['HOST'], int(dbconfig['PORT']), username=dbconfig['USER'],
                         password=dbconfig['PASSWORD'],
                         authSource=dbconfig['AUTH_SOURCE'])
    
    # Initialize the start date
    if request.GET.get('start_date') is not None:
        start_date = datetime.strptime(request.GET.get('start_date') + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(request.GET.get('end_date') + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
    else:
        start_date = datetime.today() - timedelta(days=7)
        end_date = datetime.today()
    
    # Prepare MongoDB query
    db = client[dbconfig['NAME']]
    results = db.eight2x_app_status.aggregate([
        {'$match': {
            '$and': [
                {'created_at': {'$gte': start_date}},
                {'created_at': {'$lte': end_date}}
            ]
        }},
        {'$group': {'_id': {'country': '$country', 'sentiment': '$sentiment'}, 'count': {'$sum': 1}}}
    ])
    
    # Query countrywise statistics
    stats = dict()
    for result in results:
        country = result['_id']['country'].upper()
        if country not in stats:
            stats[country] = dict(positive=0, negative=0)
        
        sentiment = result['_id']['sentiment']
        if sentiment != 'negative':
            sentiment = 'positive'
        stats[country][sentiment] = result['count']
    
    fractions = []
    for country, stat in stats.items():
        count_total = stat['positive'] + stat['negative']
        if count_total > 0:
            fraction_positive = round(stat['positive'] / count_total, 2)
            fractions.append([country, fraction_positive])
    
    data = dict()
    data['start_date'] = start_date
    data['end_date'] = end_date
    data['fractions'] = json.dumps(fractions)
    
    return render(request, 'eight2x_app/dashboard.html', data)


def tweets(request):
    """
    Send tweets by the AJAX call
    :param request:
    :return:
    """
    # Read request parameters
    start_date = datetime.strptime(request.GET.get('start_date') + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(request.GET.get('end_date') + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
    country = request.GET.get('country').lower()
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    offset = (page - 1) * limit
    
    # Prepare query
    query = dict()
    query['created_at__gte'] = start_date
    query['created_at__lte'] = end_date
    query['country'] = country
    
    if request.GET.get('sentiment') is not None:
        query['sentiment'] = request.GET.get('sentiment')
        
    if request.GET.get('promotion') is not None:
        query['promotion'] = request.GET.get('promotion')
        
    if request.GET.get('feeback') is not None:
        query['feeback'] = request.GET.get('feeback')
    
    count = Status.objects.filter(**query).count()
    results = Status.objects.filter(**query).order_by('-created_at').select_related('user')[offset:limit]
    tweets = list()
    texts = list()
    for result in results:
        tweet = result.as_dict()
        texts.append(tweet['text'].strip())
        tweets.append(tweet)
        
    # Generate summary
    summary = list()
    texts = list(set(texts))
    if len(texts) > 5:
        summarizer = FrequencySummarizer()
        summary = summarizer.summarize(texts, 5)
    
        
    total_pages = math.ceil(count / limit)
    prev_page = page > 1
    next_page = page < total_pages
    
    response = dict(count=count, tweets=tweets, prev_page=prev_page, next_page=next_page, summary=summary)
    return HttpResponse(json.dumps(response), content_type='application/json')


def statuses(request, country):
    """
    Send statuses
    :param request: request object
    :param country: selected country
    :return:
    """
    if request.GET.get('start_date') is not None:
        start_date = datetime.strptime(request.GET.get('start_date') + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(request.GET.get('end_date') + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
    else:
        start_date = datetime.today() - timedelta(days=7)
        end_date = datetime.today()
    
    data = dict()
    data['start_date'] = start_date
    data['end_date'] = end_date
    data['country'] = country
    return render(request, 'eight2x_app/statuses.html', data)


def issues(request, country):
    """
    Send statuses
    :param request: request object
    :param country: selected countr
    :return:
    """
    if request.GET.get('start_date') is not None:
        start_date = datetime.strptime(request.GET.get('start_date') + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(request.GET.get('end_date') + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
    else:
        start_date = datetime.today() - timedelta(days=7)
        end_date = datetime.today()
    
    data = dict()
    data['start_date'] = start_date
    data['end_date'] = end_date
    data['country'] = country
    return render(request, 'eight2x_app/issues.html', data)


def feedbacks(request, country):
    """
    Send statuses
    :param request: request object
    :param country: selected countr
    :return:
    """
    if request.GET.get('start_date') is not None:
        start_date = datetime.strptime(request.GET.get('start_date') + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(request.GET.get('end_date') + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
    else:
        start_date = datetime.today() - timedelta(days=7)
        end_date = datetime.today()
    
    data = dict()
    data['start_date'] = start_date
    data['end_date'] = end_date
    data['country'] = country
    return render(request, 'eight2x_app/feedbacks.html', data)


def promotions(request, country):
    """
    Send statuses
    :param request: request object
    :param country: selected countr
    :return:
    """
    if request.GET.get('start_date') is not None:
        start_date = datetime.strptime(request.GET.get('start_date') + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(request.GET.get('end_date') + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
    else:
        start_date = datetime.today() - timedelta(days=7)
        end_date = datetime.today()
    
    data = dict()
    data['start_date'] = start_date
    data['end_date'] = end_date
    data['country'] = country
    return render(request, 'eight2x_app/promotions.html', data)


def reply(request):
    pass