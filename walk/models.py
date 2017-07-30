from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Algorithm(models.Model):
    ''' Algorithm for random walk '''
    text = models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)
    	
    def __str__(self):
        ''' Return string representation of the model '''
        return self.text		

class Comment(models.Model):
    ''' description and discussion of the algorithm'''
    algorithm = models.ForeignKey(Algorithm)
    text=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ''' Return a string representation of the model '''	
        return self.text[:50] + "..."
		