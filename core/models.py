from django.db import models
from accounts.models import CustomUser

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_feedback')
    feedback = models.TextField()
