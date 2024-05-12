from django.utils import timezone

from rest_framework import serializers
from api.user.models import Teacher
from api.main.models import Attendance



class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ("season", "student", "lesson", "date", "status", "description")