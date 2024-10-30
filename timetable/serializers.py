from rest_framework import serializers
from .models import Course, Subject, Day, Period, Staff, Timetable, StaffAvailability

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description']

class SubjectSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)  
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source='course')

    class Meta:
        model = Subject
        fields = ['id', 'name', 'course', 'course_id']  

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['id', 'name']

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'


class StaffAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAvailability
        fields = ['id', 'staff', 'day', 'period']

class StaffSerializer(serializers.ModelSerializer):
    subject_ids = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), many=True, write_only=True
    )
    subjects = SubjectSerializer(many=True, read_only=True)
    availability = StaffAvailabilitySerializer(many=True, read_only=True)  

    class Meta:
        model = Staff
        fields = ['id', 'name', 'email', 'subject_ids', 'subjects', 'availability']

    def create(self, validated_data):
        subject_ids = validated_data.pop('subject_ids', [])
        staff = Staff.objects.create(**validated_data)
        staff.subjects.set(subject_ids)
        
        days = Day.objects.all()
        periods = Period.objects.all()
        
        for day in days:
            for period in periods:
                StaffAvailability.objects.create(staff=staff, day=day, period=period)

        return staff

    def update(self, instance, validated_data):
        subject_ids = validated_data.pop('subject_ids', None)
        if subject_ids is not None:
            instance.subjects.set(subject_ids)
        return super().update(instance, validated_data)

class TimetableSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    staff = StaffSerializer(read_only=True)
    day = DaySerializer(read_only=True)
    period = PeriodSerializer(read_only=True)

    class Meta:
        model = Timetable
        fields = '__all__'

