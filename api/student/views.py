from django.shortcuts import render
from django.db.models import Count, Case, When,  IntegerField
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.user.models import Student, Teacher
from api.main.models import Course, Grade, Attendance
from .permissions import IsStudent


class MyClassmatesApi(APIView):
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
            "number_of_students": Student.objects.filter(course__id = course_id).aggregate(Count('id'))['id__count']
        })
        
    

class StudentApi(APIView):
    permission_classes = (IsAuthenticated, IsStudent, )

    def get(self, request, pk, *args, **kwargs):
        try:
            # annotate,aggregate
            student = Student.objects.get(id = pk)
            
            return Response({
                "data": {
                    "id": student.id,
                    "student_id": student.student_id.int,
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "middle_name": student.middle_name,
                    "phone_number": student.phone_number,
                    "course": {
                        "id": student.course.id,
                        "name": student.course.name,
                        "leavel": student.course.leavel,
                        "letter": student.course.letter,
                    },
                    "avatar": student.avatar.url
                }
            })
        except:
            return Response({
                "error": "Bunday id li foydalanuvchi topilmadi!"
            })
    
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

        
class MyGradesApi(APIView):
    permission_classes = (IsAuthenticated, IsStudent,)

    def get_grades(self, grades: Grade):
        for grade in grades:
            yield {
                "lesson": grade['lesson__name'],
                "grade": grade['grade'],
                "description": grade['description']
            }
    
    def get(self, request, *args, **kwargs):
        try:
            date_from = request.GET.get('from').split(',')
            date_to = request.GET.get('to').split(',')
            start_date = timezone.datetime(int(date_from[0]), int(date_from[1]), int(date_from[2]))
            end_date = timezone.datetime(int(date_to[0]), int(date_to[1]), int(date_to[2]))
            grades = Grade.objects.filter(
                created__gte = start_date,
                created__lte = end_date,
                student__id = request.user.id
            ).select_related("lesson").values("lesson__name", "grade", "description")

            return Response({
                "data": self.get_grades(grades)
            })
        except:
            return Response({
                "error": "Noma'lumomt xatolik ro'y berdi!"
            })
    


class MyAttendanceApi(APIView):
    permission_classes = (IsAuthenticated, IsStudent, )

    def filter_all_date(self, data):
        now_year = timezone.now().year
        now_month = timezone.now().month
        now_day = timezone.now().day

        custom = data.get("custom", None)

        year = int(data.get("year", now_year))
        month = int(data.get("month", now_month))
        day = int(data.get("day", now_day))

        year_from = int(data.get("year[from]", now_year))
        month_from = int(data.get("month[from]", now_month))
        day_from = int(data.get("day[from]", now_day))

        year_to = int(data.get("year[to]", now_year))
        month_to = int(data.get("month[to]", now_month))
        day_to = int(data.get("day[to]", now_day))

        if (custom and custom == 'false') or not custom:
            return {
                "from_to": False,
                "year": year,
                "month": month,
                "day": day
            }
        else:
            return {
                "from_to": True,
                "year_from": year_from,
                "month_from": month_from,
                "day_from": day_from,
                "year_to": year_to,
                "month_to": month_to,
                "day_to": day_to
            }

    def get(self, request, *args, **kwargs):
        data = request.GET
        filter_all_date = self.filter_all_date(data)
        if filter_all_date['from_to']:

            start_date = timezone.datetime(
                year = filter_all_date['year_from'],
                month = filter_all_date['month_from'],
                day = filter_all_date['day_from']
            )

            end_date = timezone.datetime(
                year = filter_all_date['year_to'],
                month = filter_all_date['month_to'],
                day = filter_all_date['day_to']
            )

            attendance = Attendance.objects.filter(
                date__gte = start_date,
                date__lte = end_date,
                student__id = request.user.id
            ).select_related('student', 'season', 'lesson').aggregate(
                present_count = Count(Case(When(status='present', then=1), output_field=IntegerField())),
                absent_count = Count(Case(When(status='absent', then=1), output_field=IntegerField())),
                late_count = Count(Case(When(status='late', then=1), output_field=IntegerField())),
                excused_count = Count(Case(When(status='excused', then=1), output_field=IntegerField())),
                all_count = Count('status'),
            )

        else:
            start_date = timezone.datetime(
                year = filter_all_date['year'],
                month = filter_all_date['month'],
                day = filter_all_date['day']
            )
            attendance = Attendance.objects.filter(
                date = start_date,
                student__id = request.user.id
            ).select_related('student', 'season', 'lesson').aggregate(
                present_count = Count(Case(When(status='present', then=1), output_field=IntegerField())),
                absent_count = Count(Case(When(status='absent', then=1), output_field=IntegerField())),
                late_count = Count(Case(When(status='late', then=1), output_field=IntegerField())),
                excused_count = Count(Case(When(status='excused', then=1), output_field=IntegerField())),
                all_count = Count('status'),
            )
        return Response({
            "present": attendance['present_count'],
            "absent": attendance['absent_count'],
            "late": attendance['late_count'],
            "excused": attendance['excused_count'],
            "all": attendance['all_count'],
        })
