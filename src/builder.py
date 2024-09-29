from datetime import datetime
from pathlib import Path
from typing import Any

from models import TimeSlot, Pair, Activity, Student
from utils import xlsx_to_dict


def build_pairs(data: list[dict[str, str]], key: str = None) -> list[Pair]:
    pairs = []
    for item in data:
        if set(item.values()) == {None}:
            continue
        start_datetime = datetime.combine(
            item.get("date", datetime(2024, 1, 1, 0, 0)).date(),
            datetime.strptime(item.get("time").split("-")[0].strip(), '%H:%M').time()
        )
        finish_datetime = datetime.combine(
            item.get("date", datetime(2024, 1, 1, 0, 0)).date(),
            datetime.strptime(item.get("time").split("-")[1].strip(), '%H:%M').time()
        )
        pairs.append(
            Pair(
                time_slot=TimeSlot(start=start_datetime, finish=finish_datetime),
                activity=Activity(label=item.get("label"), link=item.get("link")),
                key=key
            )
        )

    return pairs


def load_pairs(data_path: Path) -> dict[str, list[Pair]]:
    res = {}
    general_pairs_data = xlsx_to_dict(data_path / Path("Общие пары.xlsx"))
    res["general"] = build_pairs(general_pairs_data)
    for file in data_path.glob("*_*.xlsx"):
        pair_key, group_number = file.with_suffix("").name.split("_")
        file_data = xlsx_to_dict(file)
        pairs = build_pairs(file_data, key=pair_key)
        if res.get(group_number):
            res[group_number] = res[group_number] + pairs
        else:
            res[group_number] = pairs
    return res


def assign_students(students: list[dict[str, Any]], pairs: dict[str, list[Pair]]) -> list[Pair]:
    for pair_group, pairs in pairs.items():
        for pair in pairs:
            pair_code = pair.key
            for student_dict in students:
                student = Student(name=student_dict.get("name"))
                if (str(int(student_dict.get(pair_code, -1))) == pair_group) or (pair_group == "general"):
                    pair.assign_student(student)
    return pairs


def build_individual_schedule(student: Student, all_pairs: list[Pair]) -> set[Pair]:
    res = set()
    for pair in all_pairs:
        if student.on_pair(pair):
            res.add(pair)
    return res
