from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Activity:
    label: str
    link: str

    def __eq__(self, other: 'Activity'):
        return self.label == other.label


@dataclass
class TimeSlot:
    start: datetime
    finish: datetime

    @property
    def duration(self) -> timedelta:
        return self.finish - self.start

    def intersect(self, other: 'TimeSlot') -> bool:
        return (self.start <= other.finish) and (self.finish >= other.start)

    def __and__(self, other: 'TimeSlot') -> bool:
        return self.intersect(other)


@dataclass
class Pair:
    time_slot: TimeSlot
    activity: Activity
    key: str = field(default_factory=lambda: "")
    group: set['Student'] = field(default_factory=lambda: set())

    def __hash__(self):
        return hash(self.activity.label)

    def __eq__(self, other):
        return self.activity.label == other.activity.label

    def intersect(self, other: 'Pair') -> bool:
        return self.time_slot.intersect(other.time_slot)

    def __and__(self, other: 'Pair') -> bool:
        return self.intersect(other)

    def __str__(self):
        return f"{self.activity.label} {self.time_slot.start.date()} {self.time_slot.start.time()}"

    def __repr__(self):
        return str(self)

    def assign_student(self, student: 'Student'):
        self.group.add(student)

    def to_dict(self):
        duration_hours = self.time_slot.duration.seconds // 60 // 60
        duration_minutes = self.time_slot.duration.seconds // 60 % 60
        return {
            "date": self.time_slot.start.date().strftime("%d.%m.%Y"),
            "start": self.time_slot.start.time().strftime("%H:%M"),
            "finish": self.time_slot.finish.time().strftime("%H:%M"),
            "duration": f"{duration_hours}:{duration_minutes if duration_minutes else '00'}",
            "class": self.activity.label,
            "link": self.activity.link
        }


@dataclass
class Student:
    name: str = None

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: 'Student'):
        return self.name == other.name

    def on_pair(self, pair: Pair):
        return self in pair.group
