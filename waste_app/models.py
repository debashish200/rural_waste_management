from django.db import models
from django.contrib.auth.models import User

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
    
    