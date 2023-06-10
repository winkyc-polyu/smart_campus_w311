from django.db import models

class venue_event(models.Model):
    venue = models.CharField(max_length=10)
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    event = models.CharField(max_length=10)
    instructor = models.CharField(max_length=40)
    
    def __str__(self):
        return 'venue_event #{}'.format(self.id)
    class Meta:
        verbose_name_plural = 'venue_events'
    def create(self,venue,date,time_start,time_end,event,instructor):
        self.venue =venue
        self.date =date
        self.time_start =time_start
        self.time_end =time_end
        self.event =event
        self.instructor = instructor