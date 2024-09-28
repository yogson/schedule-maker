import datetime

from models import Pair

VEVENT = """BEGIN:VEVENT
SUMMARY:{event_name}
DTSTART:{event_start_str}
DTEND:{event_end_str}
LOCATION:{event_location}
END:VEVENT
"""

ICS = """BEGIN:VCALENDAR
VERSION:2.0
{content}
END:VCALENDAR
"""


def build_ics(pairs: list[Pair]) -> str:

    vevent_list = []

    for pair in pairs:
        event_start = (pair.time_slot.start + datetime.timedelta(hours=-3)).strftime('%Y%m%dT%H%M%SZ')
        event_end = (pair.time_slot.finish + datetime.timedelta(hours=-3)).strftime('%Y%m%dT%H%M%SZ')

        vevent = VEVENT.format(
            event_name=pair.activity.label,
            event_start_str=event_start,
            event_end_str=event_end,
            event_location=pair.activity.link or ''
        )

        vevent_list.append(vevent)

    return ICS.format(content=''.join(vevent_list))

