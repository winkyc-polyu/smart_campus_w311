from django.db import models

# Create your models here.
class OnOff(models.Model):
#Fields
    state = models.CharField(max_length=3)
    date_ordered = models.DateTimeField(auto_now_add=True)
#Methods
    def __str__(self):
        return 'OnOff #{}'.format(self.id)

class BreakEvent(models.Model):
#Fields
    Break = models.CharField(max_length=5)
    date_ordered = models.DateTimeField(auto_now_add=True)
#Methods
    def __str__(self):
        return 'BreakEvent #{}'.format(self.id)