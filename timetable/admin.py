
from django.contrib import admin
from .models import Course, Subject, Staff, Day, Period, Timetable

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description') 
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course') 
    list_filter = ('course',) 
    search_fields = ('name',) 

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')  
    search_fields = ('name', 'email')  

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') 

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time')

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'day', 'period', 'subject', 'staff')
    list_filter = ('course', 'day') 
    search_fields = ('course__name', 'subject__name', 'staff__name') 
