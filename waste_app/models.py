from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Complaint(models.Model):
    STATUS_CHOICES=[('Pending','Pending'),
                    ('In Progress','In Progress'),
                    ('Resolved','Resolved')
                    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    location=models.CharField(max_length=200)
    description=models.TextField()
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')

    def __str__(self):
        return self.location
    
class Profile(models.Model):
    ROLE_CHOICE=[('admin','Admin'),
                 ('user','User')]
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=10,choices=ROLE_CHOICE)

    def __str__(self):
        return self.user.username
    
@receiver(post_save,sender=User)
def created_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    

    
    