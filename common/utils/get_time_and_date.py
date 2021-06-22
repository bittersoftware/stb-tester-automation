import stbt
import re
from datetime import timedelta
from datetime import datetime
import pytz
from enum import Enum


class MONTH(Enum):
    ene = 1
    feb = 2
    mar = 3
    abr = 4
    may = 5
    jun = 6
    jul = 7
    ago = 8
    sep = 9
    oct = 10
    nov = 11
    dic = 12


class GetTimeAndDate:
    """
    Class that returns date and time from Ajustes and sub-menu screens
    Screens inside Ajustes implements this class and are able to return the
    following properties:
        @current timme dictionaty (day: int, month: int, hour: int, minute: int)
        {
            "day": day,
            "month": month,
            "hour": hour,
            "minute": minute
        }
    """

    def __init__(self, obj):
        if obj.is_visible:
            self.obj = obj.refresh()
            self.region = stbt.Region(985, 40, width=145, height=40)
        else:
            raise ValueError("Page {} is not visible".format(obj))

    @property
    def _time_and_date_raw(self):
        region = self.region
        __time_and_date_raw = stbt.ocr(
            region=region,
            text_color_threshold=20,
            mode=stbt.OcrMode.SPARSE_TEXT_WITH_OSD,
        )

        return __time_and_date_raw

    @property
    def time_and_date_parsed(self):
        """Formats start and end time captured through OCR

        Example: "9 feb 12:52" or "21 mar 01:20"

        Due to OCR misreading text, we are handling the possible outputa cases:
        len(5) = "12:35"
        len(4) = "1235"

        Sometimes the ":" is not detected, so we slice the str accordingly the output

        Args:
            time_raw (str): time raw


        Returns:
            [dict]: containing "day", "month", "hour" and "time"
        """
        time_and_date = self._time_and_date_raw

        # 9 feb 12:52 - reads day, month, then time by reguar expression
        day = int(re.findall("^[0-9]{1,2}", time_and_date)[0])
        month = str(re.findall("[a-z]{3}", time_and_date)[0])
        time = (re.findall("[0-9]{1,2}.[0-9]{2}$", time_and_date))[0]

        if len(time) == 5:
            hour = time[0:2]
            minute = time[-2:]
        elif len(time) == 4:
            hour = time[0:1]
            minute = time[-2:]
        else:
            print("OCR failed to read time")
            return None

        try:
            hour = int(hour)
            minute = int(minute)
        except Exception as e:
            print(e, " Failed to get time")

        stb_time = {
            "day": day,
            "month": MONTH[month].value,
            "hour": hour,
            "minute": minute,
        }

        return stb_time

    @property
    def day(self):
        return self.time_and_date_parsed[0]

    @property
    def month(self):
        return self.time_and_date_parsed[1]

    @property
    def hour(self):
        return self.time_and_date_parsed[2]

    @property
    def minute(self):
        return self.time_and_date_parsed[3]


def now():
    """Returns current time and date for Spain TZ

    Returns:
        obj: datetime.now()
            obj.hour
            obj.minute
            obj.day
            obj.month
    """

    tz_spain = pytz.timezone("Europe/Brussels")
    tz_spain = datetime.now(tz_spain)

    return tz_spain


def assert_current_time_and_date(stb_time):
    """Compares current time from now() method with current time

    Args:
        data (tuple): (day, month, hour, minute)

    Raises:
        ValueError: Error Message when times do not match.

    Returns:
        True: if times match
    """
    system_date = now()

    if system_date.month != stb_time["month"]:
        print("SYSTEM ", system_date.month)
        print("STB ", stb_time["month"])
        raise ValueError(
            "Current time {} does not match expected: {}".format(now(), stb_time)
        )

    stb_hhmm = timedelta(hours=stb_time["hour"], minutes=stb_time["minute"])
    system_hhmm = timedelta(hours=system_date.hour, minutes=system_date.minute)

    delta = system_hhmm - stb_hhmm

    if abs(delta.total_seconds()) < 180:
        print("Current time {} matches expected: {}".format(now(), stb_time))
    else:
        raise ValueError(
            "Current delta {} is greater than 180s (3min)".format(delta.total_seconds())
        )
