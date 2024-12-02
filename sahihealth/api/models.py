import uuid
from django.db import models

# Create your models here.

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)  
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name
    
