# -*- coding: utf-8 -*-
import re
from datetime import timedelta
import logging

import stbt

from common.exceptions import NotInScreen
from common.utils.get_time_and_date import GetTimeAndDate
from common.utils.rcu import RCU

logger = logging.getLogger(__file__)


class Img:
    """List of reference images locators"""

    PAGE_TITLE = "./images/guia_page_title.png"
    LOGO = "./images/guia_logo.png"
    PROGRESS_BAR = "./images/guia_progress_bar.png"
    GRABAR_ICON = "./images/guia_grabar.png"
    HD_ICON = "./images/guia_hd.png"
    INICIAR_ICON = "./images/guia_iniciar.png"
    OK_ICON = "./images/guia_ok.png"
    DOLBY_ICON = "./images/guia_dolby.png"
    PARENTAL_TP = "./images/guia_parental_TP.png"
    PARENTAL_07 = "./images/guia_parental_7.png"
    PARENTAL_12 = "./images/guia_parental_12.png"
    PARENTAL_16 = "./images/guia_parental_16.png"
    PARENTAL_18 = "./images/guia_parental_18.png"


parental_list = [
    Img.PARENTAL_TP,
    Img.PARENTAL_07,
    Img.PARENTAL_12,
    Img.PARENTAL_16,
    Img.PARENTAL_18,
]


class Guide(stbt.FrameObject):
    """Page Object for Guide

    When instantiated, an image capture is done and
    de property is_visible is set to True if we are
    in Guide page.
    """

    def __bool__(self):
        return self.is_visible

    def __repr__(self):
        if self.is_visible:
            return "Guide(is_visible=True)"
        else:
            return "Guide(is_visible=False)"

    @property
    def is_visible(self):
        """Returns True if in Guide page"""

        region = stbt.Region(0, 0, width=1280, height=100)

        title = stbt.match(Img.PAGE_TITLE, frame=self._frame, region=region)

        logo = stbt.match(Img.LOGO, frame=self._frame, region=region)

        return title and logo

    @property
    def channel_number(self):

        region = stbt.Region(130, 645, width=110, height=35)

        ch = stbt.ocr(frame=self._frame, region=region, mode=stbt.OcrMode.RAW_LINE)

        try:
            return int(ch)
        except ValueError:
            return None

    @property
    def parental(self):
        """Returns parental if found

        Returns:
            string: parental rate
        """
        for parental in parental_list:
            if stbt.match(
                parental,
                frame=self._frame,
                region=stbt.Region(1080, 530, width=190, height=180),
            ):
                return re.findall(r"\d{1,2}|TP", parental)[0]

        return None

    @property
    def hd(self):
        """Returns True if HD icon is found

        Returns:
            boolean: True if HD
        """
        return (
            stbt.match(
                Img.HD_ICON,
                frame=self._frame,
                region=stbt.Region(1080, 530, width=190, height=180),
            )
        ).match

    @property
    def dolby(self):
        """Returns True if DOLBY icon is found

        Returns:
            boolean: True if DOLBY
        """
        return (
            stbt.match(
                Img.DOLBY_ICON,
                frame=self._frame,
                region=stbt.Region(1080, 530, width=190, height=180),
            )
        ).match

    @property
    def event_title(self):
        """Returns event title if DOLBY icon is found

        Returns:
            str: Title of current event
        """

        title = stbt.ocr(
            frame=self._frame,
            lang="spa",
            region=stbt.Region(340, 540, width=925, height=60),
        )

        return title

    @property
    def exihbition_times(self):
        """Returns event start time

        Returns:
            str: Event start time
        """

        start_time = stbt.ocr(
            region=stbt.Region(345, 605, width=60, height=25),
            text_color_threshold=20,
            mode=stbt.OcrMode.SPARSE_TEXT_WITH_OSD,
        )

        if stbt.match(
            Img.PROGRESS_BAR,
            frame=self._frame,
            region=stbt.Region(405, 595, width=25, height=45),
        ):

            # Current event
            end_time_region = stbt.Region(1005, 605, width=60, height=25)

        else:
            # Past or Future events
            end_time_region = stbt.Region(420, 605, width=60, height=25)

        end_time = stbt.ocr(
            region=end_time_region,
            text_color_threshold=20,
            mode=stbt.OcrMode.SPARSE_TEXT_WITH_OSD,
        )

        parsed_start_time = _format_time(start_time)
        parsed_end_time = _format_time(end_time)

        init = timedelta(
            hours=parsed_start_time["hour"], minutes=parsed_start_time["minute"]
        )
        end = timedelta(
            hours=parsed_end_time["hour"], minutes=parsed_end_time["minute"]
        )

        delta = end - init

        return {
            "start": parsed_start_time,
            "end": parsed_end_time,
            "duration": str(delta),
        }


def is_visible():
    """Check if in Guide

    Returns:
        [boolean]: [Returns True if in Guide]
    """
    guide = Guide()
    return guide.is_visible


def assert_screen():
    """Raises Exception if not in Guide

    Returns:
        [obj]: [Returns instance of page]
    """
    if is_visible():
        page = Guide()
        return page
    else:
        raise NotInScreen(__name__)


def get_parental():
    page = assert_screen()
    stbt.draw_text("Parental: {}".format(page.parental))
    return page.parental


def get_channel_number():
    page = assert_screen()
    stbt.draw_text("Channel Number: {}".format(page.channel_number))
    return page.channel_number


def open_guide():
    if not is_visible():
        stbt.press_and_wait(RCU.EPG)

    assert_screen()


def open_guide_get_channel_number():
    if not is_visible():
        stbt.press_and_wait(RCU.EPG)

    page = assert_screen()
    stbt.draw_text("Channel Number: {}".format(page.channel_number))
    return page.channel_number


def get_hd():
    page = assert_screen()
    stbt.draw_text("HD: {}".format(page.hd))
    return page.hd


def get_dolby():
    page = assert_screen()
    stbt.draw_text("Dolby: {}".format(page.dolby))
    return page.dolby


def get_event_title():
    page = assert_screen()
    stbt.draw_text(
        "Event: {}".format(page.event_title.encode("ascii", "ignore").decode("ascii"))
    )
    return page.event_title


def get_exihbition_times():
    page = assert_screen()
    stbt.draw_text("Start: {}".format(page.exihbition_times["start"]))
    stbt.draw_text("End: {}".format(page.exihbition_times["end"]))
    stbt.draw_text("Duration: {}".format(page.exihbition_times["duration"]))
    return page.exihbition_times


def get_time_and_date():
    """Returns date and time Ajustes and sub-menu screens

    Returns:
        [tuple]: (day: int, month: str, hour: int, minute: int)
    """
    g = Guide()
    t = GetTimeAndDate(g)
    return t.time_and_date_parsed


def _format_time(time_raw):
    """Formats start and end time captured through OCR
    Due to OCR misreading text, we are handling the possible outputa cases:
    len(5) = "12:35"
    len(4) = "1235"

    Sometimes the ":" is not detected, so we slice the str accordingly the output

    Args:
        time_raw (str): time raw

    Returns:
        dict: containing "hour" and "minute" keys
    """
    time = (re.findall("[0-9]{1,2}.[0-9]{2}$", time_raw))[0]

    if len(time) == 5:
        hour = time[0:2]
        minute = time[-2:]
    elif len(time) == 4:
        hour = time[0:1]
        minute = time[-2:]
    else:
        logger.error("OCR failed to read time")
        return None

    try:
        hour = int(hour)
        minute = int(minute)
    except Exception as e:
        logger.error(e, " Failed to get time")
        return None

    return {"hour": hour, "minute": minute}
