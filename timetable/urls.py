from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    SubjectViewSet,
    DayViewSet,
    PeriodViewSet,
    StaffViewSet,
    TimetableViewSet,
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'days', DayViewSet)
router.register(r'periods', PeriodViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'timetable', TimetableViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

