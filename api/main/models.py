from typing import Collection

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from api.user.models import Teacher, Student

from .enums import AttendanceEnum, WeekdaysEnum



class CustomModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Subject(CustomModel): # fan nomi 
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Course(CustomModel): # sinf nomi
    def course_letter():
        up_letters = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z"
        up_letters_list = up_letters.split(',')
        for i in up_letters_list:
            yield (i,i)

    letter = models.CharField(
        max_length=1,
        choices=course_letter()
    )
    leavel = models.PositiveIntegerField(
        validators=[MaxValueValidator(11), MinValueValidator(1)],
        default=1
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null = True)
    is_active = models.BooleanField(default=True)

    @property
    def name(self):
        return f"{self.leavel}-{self.letter}"
    
    def all_objects(self):
        try:
            course = Course.objects.get(letter = self.letter, leavel = self.leavel)
            if course:
                return True
        except:
            ...
        return False

    def validate_constraints(self, exclude: Collection[str] | None = ...) -> None:
        if self.all_objects():
            raise ValueError("Bunday nomdagi sinf mavjud")
        return super().validate_constraints(exclude)

    def __str__(self) -> str:
        return self.name

class Season(CustomModel): # mavsum yoki chorak
    name = models.CharField(
        max_length=255,
        help_text="Nomi",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    
    @property
    def end_of_season(self):
        now_date = timezone.now().date()
        return self.end_date - now_date
    
    def __str__(self) -> str:
        return self.name

class LessonTime(CustomModel): # dars vaqtlari
    name = models.CharField(
        max_length=255,
        help_text="Nomi",
    )
    start_time = models.TimeField(
        help_text="Boshlanish vaqti"
    )
    
    continuity = models.TimeField(
        help_text="Davomiyligi"
    )

    @property
    def end_time(self):
        return self.start_time + self.continuity

    
    def __str__(self) -> str:
        return self.name

class Lesson(CustomModel): # dars
    name = models.CharField(max_length=255, help_text="Dars nomi")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, help_text="Dars fani")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, help_text="Dars ustozi")    
    lesson_time = models.ForeignKey(LessonTime, on_delete=models.SET_NULL, null = True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, help_text="Sinf")
    week_day = models.CharField(max_length=50, choices=WeekdaysEnum.get_days(), default='mon')

    @property
    def lesson_status(self):
        now_time = timezone.now().time()
        end_lesson_time = self.lesson_time.end_time
        start_lesson_time = self.lesson_time.start_time
        if now_time > end_lesson_time:
            return "finished"
        if now_time < end_lesson_time  and now_time > start_lesson_time:
            return "started"
        if now_time < start_lesson_time:
            return "waiting"   

    def __str__(self) -> str:
        return self.name

class Grade(CustomModel): # baho
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.PositiveIntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        help_text="O'quvchi bahosi",
    )
    description = models.TextField(blank=True, null=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return self.student.full_name

class Attendance(CustomModel): # davomat
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="lesson_attendance")
    date = models.DateField()
    status = models.CharField(max_length=255, choices=AttendanceEnum.get_status(), default='absent')
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.student.full_name
        

