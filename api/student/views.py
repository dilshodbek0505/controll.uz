from django.shortcuts import render
from django.db.models import Count, Case, When,  IntegerField, TextField
from django.utils import timezone
from django.db import models

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.user.models import Student, Teacher
from api.main.models import Course, Grade, Attendance, Lesson
from .permissions import IsStudent

from django_filters.rest_framework import DjangoFilterBackend




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



# o'quvchining sinfdoshlari haqida ma'lumotlar
class StudentClassmatesApi(APIView):
    permission_classes = (IsAuthenticated, IsStudent, )

    def get_classmates(self, students: Student, student_id: int):
        for student in students:
            if student.id == student_id:
                continue
            yield {
                "id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "middle_name": student.middle_name,
                "avatar": student.avatar.url,
            }
        
    def get(self, request, *args, **kwargs):
        student = Student.objects.get(id = request.user.id)
        course_id = student.course.id
        classmates = Student.objects.filter(course__id = course_id)
    
        return Response({
            "data": self.get_classmates(classmates, request.user.id),
            "teacher": {
                "id": student.course.teacher.id,
                "first_name": student.course.teacher.first_name,
                "last_name": student.course.teacher.last_name,
                "phone_number": student.course.teacher.phone_number,
                "avatar": student.course.teacher.avatar.url,
            },
            "number_of_students": Student.objects.filter(course__id = course_id).count()
        })
        
# o'quvchining ma'lumotlarini yangilash
class UpdateStudentInformationApi(APIView):
    permission_classes = (IsAuthenticated, IsStudent, )

    def patch(self, request, *args, **kwargs):
        data = request.data
        avatar = data.get("avatar", None)
        if avatar:
            request.user.avatar = avatar
            request.user.save()
            return Response({
                "data": request.user.avatar.url
            })
        else:
            return Response({
                "error": "File topilmadi !"
            })

# o'quvchining darslari
class StudentLessonApi(APIView):
    permission_classes = (IsAuthenticated, IsStudent, )

    def get_lessons(self, request):
        start_date = request.query_params.get("start_date", timezone.now())
        end_date = request.query_params.get("end_date", timezone.now())
        
        student = Student.objects.get(id = request.user.id)
        lessons = Lesson.objects.filter(course_id = student.course.id).values(
            "id","name", "teacher_id", "teacher__first_name","teacher__last_name","lesson_time__start_time","lesson_time__continuity","lesson_time__name","week_day",
        )
        
        data = []
        for lesson in lessons:    
            attendances = Attendance.objects.filter(
                date__range = [start_date, end_date],
                student_id = student.id,
                lesson_id = lesson['id']
            ).values("date", "status", "description")
            
            attendance_data = []
            for attendance in attendances:
                attendance_data.append({**attendance})

            
            data.append({**lesson,"attendance": attendance_data})
        return data

    def get(self, request, *args, **kwargs):
        lessons = self.get_lessons(request)
        return Response({
            "status": True,
            "data": lessons
        })

# o'quvchining hattalik/kunlik/yilli darslari
class StudentCalendarApi(APIView):
    permission_classes = (IsAuthenticated, IsStudent, )

    def get(self, request, *args, **kwargs):
        course_id = Student.objects.get(id = request.user.id).course.id
        lessons = all_data(request, Lesson.objects.all().filter(course_id = course_id))
        data = []
        for lesson in lessons:
            data.append({**lesson})
        return Response({
            "data": data,
        })

# o'quvchining davomati
class StudentAttendanceApi(APIView):
    permission_classes = (IsAuthenticated, IsStudent, )

    def get(self, request,*args, **kwargs):
        attendances = Attendance.objects.all().filter(student_id = request.user.id)
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
            
        if start_date and end_date:
            attendances = attendances.filter(created__range = [start_date, end_date])
        
        attendances = filter_information(request, attendances)
        attendances = sort_data(request,attendances)
        attendances = select_data(request, attendances)

        data = []
        for attendance in attendances:
            data.append({**attendance})

        return Response({
            "data": data
        })

# o'quvchining baholari
class StudentGradeApi(APIView):
    def get(self, request, *args, **kwargs):
        grades = all_data(request, Grade.objects.all().filter(student_id = request.user.id))
        data = []
        for grade in grades:
            data.append({**grade})
        
        return Response({
            "data": data
        })
