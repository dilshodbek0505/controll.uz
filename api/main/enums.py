from enum import Enum

class AttendanceEnum(Enum):
    present = "present"
    absent = "absent"
    late = "late"
    excused = "excused"
    
    @classmethod
    def get_status(cls):
        return [ (status.value, status.name) for status in cls]

# Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday

class WeekdaysEnum(Enum):
    monday = 'mon'
    tuesday = 'tue'
    wednesday = 'wed'
    thursday = 'thu'
    friday = 'fri'
    # saturday = 'sat'
    # sunday = 'sun'

    @classmethod
    def get_days(cls):
        return [ (status.value, status.name) for status in cls]