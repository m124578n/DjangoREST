from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ToDoList(models.Model):
    owner = models.ForeignKey(User, related_name='to_do_list', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    del_tag = models.BooleanField(default=False)

    class Meta:
        db_table = 'to_do_list'
        ordering = ['created_date']
