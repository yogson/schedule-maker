from pathlib import Path

from openpyxl import Workbook

from models import Pair


def build_xls(data: list[Pair]) -> Workbook:
    workbook = Workbook()
    workbook.remove(workbook.worksheets[0])

    for pair in data:
        ws = workbook.create_sheet(title=f"{pair.time_slot.start.strftime('%d.%m.%Y %H-%M')} {pair.activity.label}")
        ws["A1"] = pair.activity.label
        ws["A2"] = pair.activity.link
        ws["A3"] = ""
        for i, student in enumerate(pair.group):
            ws[f"A{i+4}"] = i + 1
            ws[f"B{i+4}"] = student.name

    return workbook


def save_xls(data: Workbook, file: Path):
    data.save(file)
