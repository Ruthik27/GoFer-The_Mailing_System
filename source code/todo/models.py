from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class secure_data(models.Model):
    sender = models.TextField(blank=True)
    receiver = models.TextField(blank=True)
    data_file = models.TextField(blank=True)
    algo_type = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)    


class IMAGE_upload(models.Model): 
    Enter_Subject_of_received_data_to_encrypt_file = models.CharField(max_length=50) 
    steganography_image = models.ImageField(upload_to='static/images/') 
