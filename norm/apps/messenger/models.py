from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Habit(models.Model):
    recipient_id = models.BigIntegerField()
    content = models.TextField(blank=False)
    frequency = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Schedule(models.Model):
    habit_id = models.ForeignKey('Habit')
    hour = models.IntegerField()

class Response(models.Model):
    recipient_id = models.BigIntegerField()
    habit_id = models.ForeignKey('Habit')
    response_content = models.CharField(max_length=75, default='No Response')
    sent_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(auto_now=True)
