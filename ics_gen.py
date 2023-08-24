"""creating ical values based on class descriptions

god I hate icalendar"""

from typing import List
from icalendar import Calendar, Event
import datetime, pytz


DAYS_OF_WEEK = ["SU", "MO", "TU", "WE", "TH", "FR", "SA"]


def create_calendar() -> Calendar:
    """Create a Calendar object.

    :returns: Blank calendar"""
    return Calendar()


def create_class(cal: Calendar,
                 course_id: str,
                 name: str,
                 location: str,
                 days_of_week: List[int],
                 start: str,
                 end: str,
                 start_date: str,
                 end_date: str):
    """Add a class to the calendar.

    :param cal: Calendar to add the event to
    :param course_id: Course ID (example: "CS100")
    :param name: Long name of the course (example: "Intro to Profession")
    :param location: Location of class (example: "SB 104")
    :param days_of_week: Numeric index of day of the week (0 = Sunday, 1 = Monday, etc.)
    :param start: Start time in hh:mm format (example: "13:50")
    :param end: End time in hh:mm format (example: "15:05")
    :param start_date: Date course starts, in ISO-8601 format (example: "2023-08-21")
    :param end_date: Date course ends, in ISO-8601 format (example: "2023-12-08")"""
    e = Event()
    e['summary'] = f"{course_id} - {name}"
    e['location'] = location
    dt_start = datetime.datetime.fromisoformat(f"{start_date} {start}").replace(tzinfo=pytz.timezone("US/Central"))
    e.add("dtstart", dt_start)
    dt_end = datetime.datetime.fromisoformat(f"{start_date} {end}").replace(tzinfo=pytz.timezone("US/Central"))
    e.add("dtend", dt_end)
    rr_end = datetime.datetime.fromisoformat(f"{end_date} {end}").replace(tzinfo=pytz.timezone("US/Central"))
    e.add("RRULE", {"freq": "WEEKLY", "until": rr_end, "byday": [DAYS_OF_WEEK[i] for i in days_of_week]})
    cal.add_component(e)


def save_cal(cal: Calendar, filename: str = "result.ics"):
    """Save calendar as a file.

    :param cal: Calendar to convert and save.
    :param filename: Name of file to save (please use .ics extension!)"""
    with open(filename, "wb") as f:
        f.write(cal.to_ical())


if __name__ == "__main__":
    cal = create_calendar()

    create_class(cal,
                 "CS100",
                 "Intro to Profession",
                 "SB 104",
                 [5],
                 "13:50",
                 "15:05",
                 "2023-08-25",
                 "2023-12-08")
    create_class(cal,
                 "CS100",
                 "Intro to Profession",
                 "SB 104",
                 [3,5],
                 "10:00",
                 "11:15",
                 "2023-08-21",
                 "2023-12-08")
    print(cal.to_ical().decode("utf-8").replace('\r\n', '\n').strip())
    save_cal(cal)