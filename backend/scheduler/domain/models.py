from dataclasses import dataclass, field
from datetime import time


@dataclass(slots=True)
class TeacherSpec:
    id: int
    name: str
    seniority_level: int
    unavailable_days: set[str] = field(default_factory=set)
    unavailable_ranges: list[tuple[str, time | None, time | None]] = field(default_factory=list)


@dataclass(slots=True)
class RoomSpec:
    id: int
    code: str
    room_type: str


@dataclass(slots=True)
class TimeSlotSpec:
    id: int
    day_name: str
    slot_type: str
    start_time: time
    end_time: time
    duration_minutes: int


@dataclass(slots=True)
class CourseOfferingSpec:
    id: int
    section_id: int
    course_code: str
    course_name: str
    course_type: str
    weekly_frequency: int
    duration_minutes: int
    required_room_type: str
    eligible_teacher_ids: list[int]
    composite_group_code: str = ""


@dataclass(slots=True)
class WeightConfig:
    theory_after_1310: int = 100
    senior_teacher_morning: int = 25


@dataclass(slots=True)
class SchedulingProblem:
    section_id: int
    teachers: list[TeacherSpec]
    rooms: list[RoomSpec]
    time_slots: list[TimeSlotSpec]
    offerings: list[CourseOfferingSpec]
    weights: WeightConfig

