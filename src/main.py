from pathlib import Path
from itertools import chain

from builder import assign_students, load_pairs, build_individual_schedule
from writers.ics_writer import build_ics
from utils import xlsx_to_dict, write_file

SCHEDULES_PATH = '/Users/yogson/Documents/Семестр 2'
OUTPUT_DIR = "/Users/yogson/Documents/schedule"

if __name__ == '__main__':
    pairs = load_pairs(Path(SCHEDULES_PATH))
    students = xlsx_to_dict(Path(SCHEDULES_PATH) / Path("Список студентов.xlsx"))
    assign_students(students, pairs)
    all_pairs = list(chain(*list(pairs.values())))
    all_students = {student for pair in all_pairs for student in pair.group}
    for student in all_students:
        student_pairs = build_individual_schedule(student, all_pairs)
        write_file(build_ics(student_pairs), Path(OUTPUT_DIR) / Path(f"{student.name}.ics"))