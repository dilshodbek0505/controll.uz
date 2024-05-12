from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.user.models import Teacher
from api.main.models import Attendance, Course, Lesson
from .seralizers import AttendanceSerializer
from .permissions import IsTeacher



class AttendanceApi(APIView):
    permission_classes = (IsAuthenticated, IsTeacher, )

    def post(self, request, *args, **kwargs):
        serializer = AttendanceSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data":serializer.data
            })

        return Response({
            "error": "Xatolik!"
        })

class MyScheduleApi(APIView):
    permission_classes = (IsAuthenticated, IsTeacher, )

    def get(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(id = request.user.id)
        lessons = Lesson.objects.filter(
            teacher_id = teacher.id
        ).select_related(
            'lesson_time', 'course'
        ).values(
            'name', 'lesson_time', 'course__letter', 'course__leavel', 'week_day'
        )

        return Response({
            "data": lessons
        })

