from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ToDoList(models.Model):
    user = models.ForeignKey(User, related_name='to_do_list')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    del_tag = models.BooleanField(default=False)
    
