from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from .enums import RoleEnum
import uuid



class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=255,
        help_text="Foydalanuvchining ismi"
    )
    last_name = models.CharField(
        max_length=255,
        help_text="Foydalanuvchining familiyasi"
    )
    middle_name = models.CharField(
        max_length=255,
        help_text="Foydalanuvchining sharfi"
    )
    username = models.CharField(
        max_length=255,
        help_text="Foydalanuvchi nomi",
        unique=True,
        error_messages={
            "unique": "Foydalanuvchi nomi takrorlanmas bo'lishi keark!",
        }
    )
    
    phone_number = models.CharField(
        max_length=255,
        help_text="Foydalanuvchining telfon raqami",
        unique=True,
        error_messages={
            "unique": "Foydalanuvchi telfon raqami takrorlanmas bo'lishi keark!",
        }
    )

    avatar = models.ImageField(
        upload_to="user/image/",
        default="/user/default/user.jpg",
        blank=True,
    )

    role = models.CharField(
        max_length=255,
        help_text="Foydalanuvchining tizimdagi o'rni",
        choices=RoleEnum.get_role()
    )
    updated = models.DateTimeField(
        help_text="Taxrir qilingan vaqti",
        auto_now=True
    )

    is_staff = models.BooleanField(default=False)


    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ("first_name", "last_name", "middle_name")

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"
    
    
    def __str__(self) -> str:
        return self.full_name


class Student(User):
    course = models.ForeignKey('main.Course', on_delete=models.CASCADE, related_name="student_course")
    student_id = models.UUIDField(default=uuid.uuid4().int % 100000, editable=False, unique=True)

    def __str__(self) -> str:
        return super().__str__()   


class Teacher(User):
    subject = models.ForeignKey('main.Subject', on_delete=models.SET_NULL, null=True)
    teacher_id = models.UUIDField(default=uuid.uuid4().int % 100000, editable=False, unique=True)


    def __str__(self) -> str:
        return super().__str__()


class Parent(User):
    children = models.ManyToManyField(Student)
    parent_id = models.UUIDField(default=uuid.uuid4().int % 100000, editable=False, unique=True)


    def __str__(self) -> str:
        return super().__str__()




