from django.db import models
from django.contrib.auth.models import User

class Mission(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    end_date = models.DateField()
    budget_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    assigned_users = models.ManyToManyField(User, related_name='missions', blank=True)
    status = models.CharField(max_length=20, choices=[('not_started', 'Pas débuté'), ('in_progress', 'En cours'), ('finished', 'Fini')], default='not_started')
    solo = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Complaint by {self.user.username} on {self.mission.name}"