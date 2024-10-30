import random
import logging
from django.db import transaction
from .models import Day, Period, Course, Subject, Staff, StaffAvailability, Timetable 

logging.basicConfig(level=logging.DEBUG)

def generate_timetable():
    logging.debug("Starting timetable generation.")
    days = Day.objects.all()
    periods = Period.objects.all()
    courses = Course.objects.all()

    if not days.exists() or not periods.exists() or not courses.exists():
        return "Timetable generation requires populated Day, Period, and Course tables."
    
    with transaction.atomic():
        Timetable.objects.all().delete()  
        
        for course in courses:
            logging.debug(f"Generating timetable for course: {course.name}")
            course_timetable = {day.name: [] for day in days}

            available_subjects = list(course.subjects.all())
            subject_count = len(available_subjects)
            if subject_count == 0:
                continue
            
            total_periods_needed = len(days) * len(periods)
            subjects_to_assign = (available_subjects * (total_periods_needed // subject_count + 1))[:total_periods_needed]
            random.shuffle(subjects_to_assign)  
            
            subject_index = 0 

            for day in days:
                logging.debug(f"  Day: {day.name}")
                
                for period in periods:
                    if subject_index < len(subjects_to_assign):
                        subject = subjects_to_assign[subject_index]
                        assigned = False

                        potential_staff = subject.staff.filter(
                            availability__day=day,
                            availability__period=period,
                        ).exclude(
                            id__in=Timetable.objects.filter(day=day, period=period).values_list('staff_id', flat=True)
                        ).distinct()

                        if potential_staff.exists():
                            selected_staff = random.choice(potential_staff)
                            Timetable.objects.create(
                                course=course,
                                day=day,
                                period=period,
                                subject=subject,
                                staff=selected_staff,
                            )

                            course_timetable[day.name].append({
                                "period": f"{period.start_time} - {period.end_time}",
                                "subject": subject.name,
                                "staff": selected_staff.name
                            })
                            assigned = True
                            
                        subject_index += 1
                        if assigned:
                            continue
                    
                    course_timetable[day.name].append({
                        "period": f"{period.start_time} - {period.end_time}",
                        "subject": "Free Period",
                        "staff": None
                    })

    return "Timetables generated successfully"
