# -*- coding: utf-8 -*-
import re
from enum import IntEnum

import stbt

from common.exceptions import NotInScreen
from common.pages.ajustes import page_ajustes
from common.utils.get_time_and_date import GetTimeAndDate
from common.utils.rcu import RCU

# Relative path for images from bloqueo de canales
IMAGES_DIR = "./images/bloqueo_de_canales_"
FOCUSED_NUMBER = IMAGES_DIR + "focused.png"
BLOCKED_ICON = IMAGES_DIR + "blocked_icon.png"
ACCPEPT_CONFIRMATION = IMAGES_DIR + "accept_selected.png"
CANCEL_CONFIRMATION = IMAGES_DIR + "cancel_selected.png"

# Max channel reference for loop through channels' list
MAX_CHANNELS = 85

# Error Messages
NOT_IN_SCREEN = "Not in {}".format(__name__)


class CaptureElement(IntEnum):
    """Options to capture elements in block screen. Used by _preliminar_region()"""

    CH_NUMBER = 0
    CH_NAME = 1
    BLOCKED_ICON = 2


class BlockChannels(stbt.FrameObject):
    """Page Object for BlockChannels

    When instantiated, an image capture is done and
    de property is_visible is set to True if we are
    in BlockChannels page.
    """

    def __bool__(self):
        return self.is_visible

    def __repr__(self):
        if self.is_visible:
            return "BlockChannels(is_visible=True)"
        else:
            return "BlockChannels(is_visible=False)"

    def __str__(self):
        return "Bloqueo de canales"

    @property
    def is_visible(self):
        """Returns True if in BlockChannels page"""
        title = "Bloqueo de canales"
        region = stbt.Region(60, 30, width=390, height=55)

        return stbt.match_text(
            title,
            frame=self._frame,
            region=region,
            mode=stbt.OcrMode.SPARSE_TEXT_WITH_OSD,
            lang="spa",
        )

    @property
    def ch_number_focused(self):
        """Returns the selected channel number

        Returns:
            [int]: channel number
        """
        region = _preliminar_region(FOCUSED_NUMBER, CaptureElement.CH_NUMBER)

        if region:
            channel = stbt.ocr(
                frame=self._frame,
                region=stbt.Region(
                    region[0], region[1], width=region[2], height=region[3]
                ),
                mode=stbt.OcrMode.RAW_LINE,
            )

            corrections = {re.compile(r"[oO]"): "0"}

            try:
                ch = int(apply_ocr_corrections(channel, corrections=corrections))
            except Exception as e:
                print(e, " Failed to get channel")

            return ch

        else:
            print("Channel not detected by OCR")
            return None


def is_in_page():
    """Check if in BlockChannels

    Returns:
        [boolean]: [Returns True if in BlockChannels]
    """
    page = BlockChannels()
    return page.is_visible


def assert_screen():
    """Raises Exception if not in BlockChannels

    Returns:
        [obj]: [Returns instance of page]
    """
    if is_in_page():
        page = BlockChannels()
        return page
    else:
        raise NotInScreen(__name__)


def navigate_to_channel(channel):
    """Navigates down to channel list until reach some of the following conditions:
        - finds target channel
        - reaches the MAX_CHANNELS navigation repetition
        - current channel is bigger than target

    Args:
        channel (int): target channel number

    Returns:
        [boolean]: True if channl is found
    """
    screen = assert_screen()

    stbt.draw_text("Navigating to channel {}".format(channel))

    for _ in range(MAX_CHANNELS):
        if screen.ch_number_focused == channel:
            ch_name = _channel_name()
            print("Channel {} - {} found".format(channel, ch_name))
            stbt.draw_text("Channel {} - {} found".format(channel, ch_name))
            return True
        elif screen.ch_number_focused < channel:
            stbt.press_and_wait(RCU.DOWN.value, stable_secs=0.2)
        else:
            print("WARNING: Channel {} not found".format(channel))
            return False

        screen = screen.refresh()

    print("WARNING: Channel {} not found".format(channel))
    return False


def block_channel():
    """Blocks focused channel inside Bloqueo de canales"

    Raises:
        ValueError: Not in BlockChannels page
        ValueError: Not possible to block channel
    """
    assert_screen()

    if not _is_blocked():
        stbt.press_and_wait(RCU.OK.value, stable_secs=0.5)
        if not _is_blocked():
            raise AssertionError("Not possible to block channel")


def unblock_channel():
    """Unblocks focused channel inside Bloqueo de canales"

    Raises:
        ValueError: Not in BlockChannels page
        ValueError: Not possible to unblock channel
    """
    assert_screen()

    if _is_blocked():
        stbt.press_and_wait(RCU.OK.value, stable_secs=0.5)
        if _is_blocked():
            raise AssertionError("Not possible to block channel")


def confirm_changes_popup(save_changes=True):
    """Access confirmation popup and allows to confirm or cancel changes."

    Args:
        save_changes (bool, optional): Saves or not the changes made. Defaults to True.
    """
    assert_screen()

    region = stbt.Region(515, 390, width=245, height=75)

    if not stbt.wait_until(
        lambda: stbt.match(ACCPEPT_CONFIRMATION, region=region)
        or stbt.match(CANCEL_CONFIRMATION, region=region),
        timeout_secs=0.5,
    ):
        stbt.press_and_wait(RCU.EXIT.value, stable_secs=0.5)

    if page_ajustes.is_visible():
        return

    if save_changes:
        stbt.press_until_match(
            RCU.RIGHT.value, ACCPEPT_CONFIRMATION, interval_secs=1, max_presses=3
        )
        stbt.press_and_wait(RCU.OK.value, stable_secs=0.5)
    else:
        stbt.press_until_match(
            RCU.RIGHT.value, CANCEL_CONFIRMATION, interval_secs=1, max_presses=3
        )
        stbt.press_and_wait(RCU.OK.value, stable_secs=0.5)

    page_ajustes.assert_screen()


def _preliminar_region(img, target=CaptureElement.CH_NUMBER):
    """Auxiliar function to fin focused channel based in image recognition
    of the blue color channel

    Args:
        img (png): Image ot be used to find a reference point in the screen
        to apply offset
        target (str, optional): [description]. Defaults to CaptureElement.CH_NUMBER.

    Returns:
        [type]: [description]
    """
    reg_x = 100
    reg_width = 60
    region = stbt.Region(reg_x, 135, width=reg_width, height=458)
    confirm_method = stbt.ConfirmMethod("absdiff")

    match = stbt.MatchParameters(
        match_method=None,
        match_threshold=None,
        confirm_method=confirm_method,
        confirm_threshold=None,
        erode_passes=None,
    )

    preliminar = stbt.match(img, region=region, match_parameters=match)

    if preliminar.region and target == CaptureElement.CH_NUMBER:
        x = reg_x
        y = preliminar.region.y - 20
        w = reg_width
        h = 45

        return (x, y, w, h)

    elif preliminar.region and target == CaptureElement.CH_NAME:
        x = reg_x + 70
        y = preliminar.region.y - 20
        w = reg_width + 230
        h = 45

        return (x, y, w, h)

    elif preliminar.region and target == CaptureElement.BLOCKED_ICON:
        x = 0
        y = preliminar.region.y - 20
        w = 120
        h = 45

        return (x, y, w, h)

    else:
        return None


def _channel_name():
    region = _preliminar_region(FOCUSED_NUMBER, target=CaptureElement.CH_NAME)

    if region:
        return stbt.ocr(
            region=stbt.Region(region[0], region[1], width=region[2], height=region[3]),
            mode=stbt.OcrMode.SPARSE_TEXT_WITH_OSD,
        )

    return None


def _is_blocked():
    region = _preliminar_region(FOCUSED_NUMBER, target=CaptureElement.BLOCKED_ICON)

    if region:
        return stbt.match(
            BLOCKED_ICON,
            region=stbt.Region(region[0], region[1], width=region[2], height=region[3]),
        )

    return None


def get_time_and_date():
    """Returns date and time Ajustes and sub-menu screens

    Returns:
        [tuple]: (day: int, month: str, hour: int, minute: int)
    """
    b = BlockChannels()
    t = GetTimeAndDate(b)
    return t.time_and_date_parsed


PatternType = type(re.compile(""))


def apply_ocr_corrections(text, corrections=None):
    """Applies the same corrections as `stbt.ocr`'s ``corrections`` parameter.
    This is available as a separate function so that you can use it to
    post-process old test artifacts using new corrections.
    :param str text: The text to correct.
    :param dict corrections: See `stbt.ocr`.
    """
    if corrections:
        text = _apply_ocr_corrections(text, corrections)
    return text


def _apply_ocr_corrections(text, corrections):
    def replace_string(matchobj):
        old = matchobj.group(0)
        new = corrections[old]
        print("ocr corrections: %r -> %r" % (old, new))
        return new

    def replace_regex(matchobj):
        new = corrections[matchobj.re]
        print("ocr corrections: /%s/ -> %r" % (matchobj.re.pattern, new))
        return new

    # Match plain strings at word boundaries:
    pattern = "|".join(
        r"\b(" + re.escape(k) + r")\b" for k in corrections if isinstance(k, basestring)
    )
    if pattern:
        text = re.sub(pattern, replace_string, text)

    # Match regexes:
    for k in corrections:
        if isinstance(k, PatternType):
            text = re.sub(k, replace_regex, text)
    return text
