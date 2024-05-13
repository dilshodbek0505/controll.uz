from django.urls import path

from .views import (
    TeacherDashboardApi,
    TeacherJournalApi,
    TeacherCalendarApi,
)


urlpatterns = [
    path('dashboard/',TeacherDashboardApi.as_view()),
    path('journal/', TeacherJournalApi.as_view()),
    path('calendar/', TeacherCalendarApi.as_view())
]
