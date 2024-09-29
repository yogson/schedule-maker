from pathlib import Path
from itertools import chain
from os import environ

from builder import assign_students, load_pairs, build_individual_schedule
from writers.ics_writer import build_ics
from utils import xlsx_to_dict, write_file
from writers.xls_writer import save_xls, dict_to_xlsx

SCHEDULES_PATH = environ.get("SCHEDULES_PATH", "./")
OUTPUT_DIR = environ.get("OUTPUT_DIR", "./")

students_list_file_name = "Список студентов.xlsx"

if __name__ == '__main__':
    pairs = load_pairs(Path(SCHEDULES_PATH))
    students = xlsx_to_dict(Path(SCHEDULES_PATH) / Path(students_list_file_name))
    assign_students(students, pairs)
    all_pairs = sorted(chain(*list(pairs.values())), key=lambda x: x.time_slot.start)
    all_students = {student for pair in all_pairs for student in pair.group}
    for student in all_students:
        student_pairs = build_individual_schedule(student, all_pairs)
        write_file(build_ics(student_pairs), Path(OUTPUT_DIR) / Path(f"{student.name}.ics"))
        save_xls(dict_to_xlsx(
            list(map(lambda x: x.to_dict(), student_pairs))),
            Path(OUTPUT_DIR) / Path(f"{student.name}.xlsx")
        )