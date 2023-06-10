from django.shortcuts import render,redirect
from .models import venue_event
from .form import loc_form
import pandas as pd
from django.db.models import Avg,Max,Min
import datetime

#pip install django-import-export

# Create your views here.

def list(request):
    entries = venue_event.objects.all()  
    if len(entries)<1:
        df = pd.read_excel(r'D:\TM1118\web\venue_data\Venue-Event (Group A).xlsx')
        df.columns=df.iloc[0]
        df=df.drop(0)
        for rows in range(51):
            new_venue_event = venue_event()
            venue = df.iloc[rows,0]
            date = df.iloc[rows,1]
            time_start = df.iloc[rows,2]
            time_end = df.iloc[rows,3]
            event = df.iloc[rows,4]
            instructor = df.iloc[rows,5]
            temp = {'venue':venue,'date':date,'time_start':time_start,'time_end':time_end,'event':event,'instructor':instructor}
            new_venue_event.create(venue,date,time_start,time_end,event,instructor)
            new_venue_event.save()
    
    #for i in loc_list:
        #new_data = venue_event.objects.filter(node_loc= loc_list).aggregate(avg_temp = Avg("temp"), min_temp=Min("temp"), max_temp= Max("temp"), max_date_created= Max("date_created"))
    #entries = {}
    context = {'entries' : entries} # Store the data in "context" dictionaries
    print(context)
    return render(request, 'event/list.html', context) # Pass the context to HTML template

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