from django.db import models
import uuid
from Auth.models import CustomUser 

class Notes(models.Model):
    N_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    U_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ForeignKey to link with the User model
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)  # Automatically updated on each save

# Create your models here.
