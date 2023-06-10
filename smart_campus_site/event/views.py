from django.shortcuts import render
from .models import venue_event
import os
import json
from django.conf import settings
import pandas as pd
import datetime

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
    # for v in venues:
    #     venue = v.venue
    #     date = v.date
    #     time = (v.time_start, v.time_end)
    #     selection[venue] = [dic]
    #     print(selection)

    selection = {
        "W311a": [{
            "2023-34-23": [("start", "end"),("start", "end")

            ],
            "2023-34-21": [("start", "end"),("start", "end")
            ]
        }],
        "W311b": [{
            "2023-34-23": [("start", "end"),("start", "end")

            ],
            "2023-34-21": [("start", "end"),("start", "end")
            ]
        }]
    }

    print(selection)

    context = {'selection' : json.dumps(selection)}
    return render(request, 'event/index.html', context)

def form_input(request):
    if request.method == 'POST':
        input_loc = request.POST.get('location')
        input_date = int(request.POST.get('date'))
        input_start = int(request.POST.get('start'))
        input_end = int(request.POST.get('end'))

        if input_loc:
            d = datetime.date(2023,6,input_date)
            dt_start = datetime.time(input_start,0,0)
            dt_end = datetime.time(input_start,0,0)
            output_data = venue_event.objects.filter(venue=input_loc,date=d,time_end__gte = dt_start,time_start__lte = dt_end).values()
            
            context = {'entries' : output_data}
            return render(request, 'event\list.html', context)  