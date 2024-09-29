from pathlib import Path

from openpyxl import Workbook


def dict_to_xlsx(data: list[dict]) -> Workbook | None:
    workbook = Workbook()
    sheet = workbook.active

    if not data:
        return

    headers = list(data[0].keys())
    sheet.append(headers)

    for row in data:
        sheet.append([row.get(header, '') for header in headers])

    return workbook


def save_xls(data: Workbook, file: Path):
    data.save(file)
