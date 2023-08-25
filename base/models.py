from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User,on_delete = models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True) # when on delete is NULL so null = True should be written
    name = models.CharField(max_length=200) #null= False is default, not allowed Null
    description = models.TextField(null = True, blank = True, max_length = 3000) # allowed Null in column
    # participants = 
    updated = models.DateTimeField(auto_now = True) #takes every save
    created = models.DateTimeField(auto_now_add = True) #takes when it s created


    class Meta:
        ordering = ['-updated','-created']
        # 'updated': Ascending order  '-updated': Descending Order

    def __str__(self):
        return self.name #in order to see name from db

class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE) #from built in User table
    room = models.ForeignKey(Room, on_delete = models.CASCADE) #models.SET_NULL room deleted-messages will be NULL connected, models.CASCADE room deleted-messages deleted
    body = models.TextField(max_length= 3000)
    updated = models.DateTimeField(auto_now = True) #takes every save
    created = models.DateTimeField(auto_now_add = True) #takes when it s created

    def __str__(self):
        return self.body[0:50]

    

