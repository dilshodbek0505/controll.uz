from enum import Enum



class RoleEnum(Enum):
    admin = 'admin'
    student = 'student'
    teacher = 'teacher'
    parent = 'parent'
    
    @classmethod
    def get_role(cls):
        return [
            (i.name, i.value) for i in cls
        ]
