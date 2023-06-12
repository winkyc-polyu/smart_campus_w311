from django.shortcuts import render
from .models import venue_event
from sensor.models import Sensor
import os
import json
from django.conf import settings
import pandas as pd
import datetime
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Avg

#pip install django-import-export

def index(request):
    venues = venue_event.objects.all()
    if len(venues) < 1:
        df = pd.read_excel(os.path.join(settings.BASE_DIR, 'Venue-Event (Group A).xlsx'))
        df = df.drop(0)
        
        for row in range(df.shape[0]):
            new_venue_event = venue_event()

            venue = df.iloc[row, 0]
            date = df.iloc[row, 1]
            time_start = df.iloc[row, 2]
            time_end = df.iloc[row, 3]
            event = df.iloc[row, 4]
            instructor = df.iloc[row, 5]
            
            new_venue_event.create(venue, date, time_start, time_end, event, instructor)
            new_venue_event.save()
        venues = venue_event.objects.all()

    selection = {}
    for v in venues:
        venue = v.venue
        date = str(v.date)
        time = (str(v.time_start), str(v.time_end))

        if venue in selection:
            if date not in selection[venue]:
                selection[venue][date] = []
            selection[venue][date].append(time)
        else:
            selection[venue] = {}
            selection[venue][date] = []
            selection[venue][date].append(time)

    

    # selection = {
    #     "W311a": {
    #         "2023-34-23": [("start", "end"),("start", "end")

    #         ],
    #         "2023-34-21": [("start", "end"),("start", "end")
    #         ]
    #     },
    #     "W311b": {
    #         "2023-34-23": [("start", "end"),("start", "end")

    #         ],
    #         "2023-34-21": [("start", "end"),("start", "end")
    #         ]
    #     }
    # }

    context = {'selection' : json.dumps(selection)}
    return render(request, 'event/index.html', context)

def getVenueData(request):
    if request.method == 'GET':
        venue = request.GET.get('venue')
        date = request.GET.get('date')
        time = request.GET.get('time')
        time = time.split(",")
        time_start = time[0]
        time_end = time[1]

        # result = venue_event.objects.filter(venue=venue, date=date)
        result = venue_event.objects.filter(venue=venue, date=date, 
            time_start=time_start, time_end=time_end)

        data = serializers.serialize('json', result)
        return JsonResponse(data, safe=False)

def temp_info(request):
    info = venue_event.objects.all().annotate(avg_temp=Avg('temp'),)
    context = {'info' : info}
    return render(request, 'event.html', context)