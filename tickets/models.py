from django.db import models
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def createtoken(sender,instance,created , **kwargs):
    if created:
        Token.objects.create(user=instance)

class Movie (models.Model):
    hall= models.CharField(max_length=20)
    movie=models.CharField(max_length=20,unique=True)
    date=models.DateField()
    
    
    def __str__(self) -> str:
        return self.movie
    
class Guest(models.Model):
    name= models.CharField(max_length=40 , null= False , blank=False)
    phone_number=models.CharField(max_length=15)
    
        
    def __str__(self) -> str:
        return self.name
    
    
class Reservation(models.Model):
    guest= models.ForeignKey(Guest , related_name='reservation', on_delete=models.CASCADE)    
    movie= models.ForeignKey(Movie , related_name='reservation', on_delete=models.CASCADE)    
    def __str__(self) -> str:
        return self.guest.name
    

    
