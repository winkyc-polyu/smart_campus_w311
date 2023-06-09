from django.db import models

class sensor(models.Model):
    
    node_id = models.CharField(max_length=3)
    node_loc = models.CharField(max_length=10)

    temp = models.CharField(max_length=5)
    hum = models.CharField(max_length=5)
    light = models.CharField(max_length=5)
    snd = models.CharField(max_length=5)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Sensor #{}'.format(self.id)