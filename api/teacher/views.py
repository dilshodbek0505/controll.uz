from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.user.models import Teacher, Student
from api.main.models import Attendance, Course, Lesson, Season, LessonTime, Grade
from .permissions import IsTeacher

from datetime import datetime, timedelta




def select_data(request, queryset):
    data = request.query_params.get('_select')
    if data:
        data = data.split(',')
        query_fields = []
        for field in data:
            query_fields.append(field)
        return queryset.values(*query_fields)
     
    return queryset.values()
   
def sort_data(request, queryset):
    data = request.query_params.get("sortBy")
    if data:
        data = data.split(',')
        return queryset.order_by(*data)
    return queryset

def filter_date(request, queryset):
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
        
    if start_date and end_date:
        return queryset.filter(created__range = [start_date, end_date])
    
    return queryset

def filter_information(request, queryset):
    ignore_keys = ["start_date", "end_date","sortBy", "_select"]
    query_params_items = request.query_params.items()
    query_fields = {}

    for key, value in query_params_items:
        if key in ignore_keys:
            continue
        query_fields[key] = value

    return queryset.filter(**query_fields)

def all_data(request, queryset):
    queryset_filters_by_date = filter_date(request, queryset)
    order_queryset_with_infromation = sort_data(request, queryset_filters_by_date)
    filter_queryset_with_values = filter_information(request,order_queryset_with_infromation)
    res = select_data(request, filter_queryset_with_values)

    return res


class TeacherDashboardApi(APIView):
    permission_classes = (IsAuthenticated, IsTeacher, )

    def post(self, request, *args, **kwargs):
        data = request.data
        status = data.get("status")
        if status:
            lesson_id = data.get("lesson_id")
            lesson = Lesson.objects.get(id = lesson_id)
            lesson.lesson_status = status
            lesson.save()
            data = []
            studnets = Student.objects.filter(
                course_id = lesson.course.id
            ).values("id", "first_name", "last_name", "middle_name")
            for student in studnets:
                data.append({**student})
        
        return Response({
            "status": True,
            "data": data
        })
    
    def get(self, request, *args, **kwargs):
        today = datetime.now().date()# - timedelta(days=1)
        weekday_number = datetime.now().weekday()
        weekday = ["mon","tue", "wed", "thu", "fri","sut", "sun"]
        teacher = Teacher.objects.get(id = request.user.id)

        lessons = Lesson.objects.filter(
            # week_day = weekday[1],
            week_day = weekday[weekday_number],
            teacher_id = teacher.id

        )

        data = []
        for lesson in lessons:
            data.append({
                "id": lesson.id,
                "name": lesson.name,
                "course": lesson.course.name,
                "start_time": lesson.lesson_time.start_time,
                "end_time": lesson.lesson_time.end_time,
                "status": lesson.lesson_status,
            })

        return Response({
            "status": True,
            "date": datetime.now().date(), 
            "data": data
        })

class TeacherJournalApi(APIView):
    permission_classes = (IsAuthenticated, IsTeacher,)
    
    def post(self, request, *args, **kwargs):
        today = datetime.now().date()
        data = request.data
        dates = data.get("data")
        lesson_id = data.get("lesson_id")
        current_season = Season.objects.filter(start_date__lte=today, end_date__gte=today).first()
        
        for d in dates:
            attendance,_ = Attendance.objects.update_or_create(
                student_id = d['id'],
                lesson_id = lesson_id,
                date = today,
                season_id = current_season.id,
                defaults={
                    "status": d['attendance']
                }
            )  
            grade,_ = Grade.objects.update_or_create(
                student_id = d['id'],
                lesson_id = lesson_id,
                date = today,
                season_id = current_season.id,
                defaults={
                    "grade" : d['grade']
                }
                
            )
            attendance.save()
            grade.save()
    

        return Response({
            "status": True,
        })

class TeacherCalendarApi(APIView):
    permission_classes = (IsAuthenticated, IsTeacher, )

    def get(self, request, *args, **kwargs):
        teacher_id = Teacher.objects.get(id = request.user.id)
        lessons = all_data(request, Lesson.objects.all().filter(teacher_id = teacher_id))
        data = []
        for lesson in lessons:
            data.append({**lesson})
        return Response({
            "data": data,
        })
    