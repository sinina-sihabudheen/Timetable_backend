from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Subject, Day, Period, Staff, Timetable
from .serializers import (
    CourseSerializer,
    SubjectSerializer,
    DaySerializer,
    PeriodSerializer,
    StaffSerializer,
    TimetableSerializer,
)
from .generator import generate_timetable  


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class DayViewSet(viewsets.ModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializer


class PeriodViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer

    @action(detail=False, methods=['get'])
    def generate(self, request):
        generate_timetable() 
        timetables = Timetable.objects.all()
        serializer = self.get_serializer(timetables, many=True)
        return Response(serializer.data)