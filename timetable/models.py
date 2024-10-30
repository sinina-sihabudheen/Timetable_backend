from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Day(models.Model):
    name = models.CharField(max_length=10)  

    def __str__(self):
        return self.name


class Period(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subjects = models.ManyToManyField(Subject, related_name="staff")

    def __str__(self):
        return self.name


class StaffAvailability(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="availability")
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('staff', 'day', 'period')  


class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="timetables")
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.course.name} - {self.day.name} - {self.period}"
