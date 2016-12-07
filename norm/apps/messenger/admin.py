from django.contrib import admin
from models import Response, Habit, Schedule

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient_id', 'habit_id', 'response_content', 'sent_at', 'responded_at')

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient_id', 'frequency', 'created_at')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('habit_id', 'hour')

