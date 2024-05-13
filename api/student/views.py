from django.shortcuts import render
from django.db.models import Count, Case, When,  IntegerField, TextField
from django.db import models

from datetime import datetime, timedelta

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

# student haqida ma'lumot
class StudentApi(APIView):
    permission_classes = (IsAuthenticated, IsStudent, )
    def get(self,request, *args, **kwargs):
        student = Student.objects.get(id = request.user.id)
        
        return Response({
            "data": {
                "id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "phone_number": student.phone_number,
                "avatar": student.avatar.url,
            }
        })

# student dashboard
class StudentDashboardApi(APIView):
    permission_classes = (IsAuthenticated, IsStudent, )

    def get(self, request, *args, **kwargs):
        today = datetime.now().date()# - timedelta(days=1)
        weekday_number = datetime.now().weekday()
        weekday = ["mon","tue", "wed", "thu", "fri","sut", "sun"]
        student = Student.objects.get(id = request.user.id)

        lessons = Lesson.objects.filter(
            # week_day = weekday[1],
            week_day = weekday[weekday_number],
            course_id = student.course.id,
        )
        
        data = []
        for lesson in lessons:
            attendance = None
            try:
                attendance = Attendance.objects.get(
                    date = today,
                    student_id = student.id,
                    lesson_id = lesson.id,   
                ).status
            except:
                ...
            
            grade = None
            try:
                grade = Grade.objects.get(
                    date = today,
                    student_id = student.id,
                    lesson_id = lesson.id,   
                ).grade
            except:
                ...

        

            data.append({
                "id": lesson.id,
                "name": lesson.name,
                "start_time": lesson.lesson_time.start_time.strftime("%H:%M"),
                "end_time": lesson.lesson_time.end_time.strftime("%H:%M"),
                "status": lesson.lesson_status,
                "teacher": {
                    "id": lesson.teacher.id,
                    "first_name": lesson.teacher.first_name,
                    "last_name": lesson.teacher.last_name,
                    "middle_name": lesson.teacher.middle_name,
                    "full_name": lesson.teacher.full_name,
                    "phone_number": lesson.teacher.phone_number,
                },
                "attendance": attendance,
                "grade": grade,
            })

        return Response({
            "status": True,
            "date": datetime.now().date(), 
            "data": data
        })
    
# student analytics
class StudentAnalyticsApi(APIView):
    permission_classes = (IsAuthenticated, IsStudent, )
    

    def count_attendance_status(self,lessons, student):
        annotated_lessons = Lesson.objects.filter(id__in=[lesson.id for lesson in lessons]).annotate(
            present_count=Count('lesson_attendance', filter=models.Q(lesson_attendance__student=student, lesson_attendance__status='present')),
            absent_count=Count('lesson_attendance', filter=models.Q(lesson_attendance__student=student, lesson_attendance__status='absent')),
            late_count=Count('lesson_attendance', filter=models.Q(lesson_attendance__student=student, lesson_attendance__status='late')),
            excused_count=Count('lesson_attendance', filter=models.Q(lesson_attendance__student=student, lesson_attendance__status='excused'))
        )
        status_counts = {}
        for lesson in annotated_lessons:
            
            status_counts[lesson.name] = {
                'teacher': lesson.teacher.full_name,
                'present': lesson.present_count,
                'absent': lesson.absent_count,
                'late': lesson.late_count,
                'excused': lesson.excused_count,
                "all": lesson.present_count + lesson.absent_count + lesson.late_count
            }
        return status_counts

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(id = request.user.id)
        lessons = Lesson.objects.all()
        print(self.count_attendance_status(lessons,student))

        return Response({
            "status": True,
            "data": self.count_attendance_status(lessons,student)
        })



