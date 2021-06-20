# -*- coding: utf-8 -*-
import re
import time

import stbt

from common.exceptions import NotInScreen
from common.pages.guia import page_guia
from common.pages.home import page_home
from common.pages.pin import page_pin
from common.utils.rcu import RCU

# Relative path for images from live miniguide and other elements
IMAGES_DIR = "./images/en_vivo_"
MINIGUIDE = IMAGES_DIR + "mini_guide.png"
PROGRESS_BAR = IMAGES_DIR + "progress_bar.png"
CHANNEL_FOCUS = IMAGES_DIR + "channel_focus.png"
ENVENTANAR_FOCUS = IMAGES_DIR + "enventanar_focus.png"
SUGERENCIAS_FOCUS = IMAGES_DIR + "sugerencias_focus.png"
MINIGUIDE_FOCUS = IMAGES_DIR + "mini_guide_focus.png"
PAUSE_ICON = IMAGES_DIR + "pause.png"
SUGERENCIAS_ICON = IMAGES_DIR + "sugerencias_icon.png"
ENVENTANAR_ICON = IMAGES_DIR + "enventanar_icon.png"
GRABAR_ICON = IMAGES_DIR + "grabar.png"
HD_ICON = IMAGES_DIR + "hd.png"
INICIAR_ICON = IMAGES_DIR + "iniciar.png"
OK_ICON = IMAGES_DIR + "ok.png"
PARENTAL_TP = IMAGES_DIR + "parental_TP.png"
PARENTAL_07 = IMAGES_DIR + "parental_7.png"
PARENTAL_12 = IMAGES_DIR + "parental_12.png"
PARENTAL_16 = IMAGES_DIR + "parental_16.png"
PARENTAL_18 = IMAGES_DIR + "parental_18.png"
MOTION_MASK = IMAGES_DIR + "motion_mask.png"

parental_list = [PARENTAL_TP, PARENTAL_07, PARENTAL_12, PARENTAL_16, PARENTAL_18]


# Error messages
NOT_IN_SCREEN = "Not in {}".format(__name__)


class EnVivo(stbt.FrameObject):
    """Page Object for EnVivo

    When instantiated, an image capture is done and
    de property is_visible is set to True if we are
    in EnVivo page.
    """

    def __bool__(self):
        return self.is_visible

    def __repr__(self):
        if self.is_visible:
            return "EnVivo(is_visible=True)"
        else:
            return "EnVivo(is_visible=False)"

    @property
    def is_visible(self):
        """Returns True if in EnVivo page"""

        region1 = stbt.Region(300, 525, width=45, height=40)

        region2 = stbt.Region(308, 640, width=660, height=75)

        bar = stbt.match(
            PROGRESS_BAR, frame=self._frame, match_parameters=None, region=region1
        )

        ok = stbt.match(
            OK_ICON, frame=self._frame, match_parameters=None, region=region2
        )

        return bar and ok

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
                match_parameters=None,
                region=stbt.Region(244, 470, width=750, height=70),
            ):
                return re.findall(r"\d{1,2}|TP", parental)[0]

        return None

    @property
    def channel_number(self):
        """Returns channel number if found

        Returns:
            int: channel
        """
        ch = stbt.ocr(region=stbt.Region(77, 505, width=135, height=55))

        try:
            return int(ch)
        except ValueError:
            return None


def is_visible():
    """Check if in EnVivo Miniguide

    Returns:
        [boolean]: [Returns True if in EnVivo]
    """
    en_vivo = EnVivo()

    if not en_vivo.is_visible:
        stbt.press(RCU.OK.value)
        time.sleep(1)

    en_vivo = en_vivo.refresh()

    return en_vivo.is_visible


def assert_screen():
    """Raises Exception if not in EnVivo

    Returns:
        [obj]: [Returns instance of page]
    """
    if is_visible():
        page = EnVivo()
        return page
    else:
        raise NotInScreen(__name__)


def parental():
    """Returns the parental rating of the live event."
        Checks if is in live (miniguide).
        If not, tries to open miniguide.

        Gets parental rating from miniguide:
        - TP
        - 7
        - 12
        - 16
        - 18

    Returns:
        string: parental rate
    """
    screen = assert_screen()

    return screen.parental


def zap_to_ch(ch, unblock=True, pin=None):
    """Zaps to desired channel from live

    Args:
        ch (list): int channel number
        unblock (bool, optional): True if willing to try to unblock channel.
        Defaults to True.
        pin (list, optional): list of ints with pin (Ex: [1,1,1,1]). Defaults to None.

    Returns:
        boolean: True if matches desired channel
    """

    digit_list = [int(i) for i in str(ch)]

    assert len(digit_list) <= 3, "Invalid number of digits. Must be 3 digits"
    assert all(
        isinstance(digit, int) for digit in digit_list
    ), "All digits must be integers"
    assert all(
        0 <= digit <= 9 for digit in digit_list
    ), "All digits must be in range 0-9"

    go_to_live()

    assert_screen()

    converted_digit_list = _convert_ch_list(digit_list)

    for index, digit in enumerate(converted_digit_list):
        stbt.press(digit)
        time.sleep(0.5)

    time.sleep(5)

    _check_live_state(unblock, pin)

    if get_channel_number() == ch:
        stbt.draw_text(
            "SUCCESS: TARGET CH {}, CURRENT CH {},".format(ch, get_channel_number())
        )
        stbt.press_and_wait(
            RCU.EXIT.value,
            region=stbt.Region(310, 645, width=60, height=70),
            stable_secs=0.5,
        )
        return True
    else:
        stbt.draw_text(
            "FAIL: TARGET CH {}, CURRENT CH {}".format(ch, get_channel_number())
        )
        stbt.press_and_wait(
            RCU.EXIT.value,
            region=stbt.Region(310, 645, width=60, height=70),
            stable_secs=0.5,
        )
        return False


def go_to_live(unblock=True, pin=None):
    """Go to live if accessible from Home Screen
    Allows unblock channel if detects PIN screen is disabled
    If unblock=True and pin is None, default pin is inserted

    Args:
        unblock (bool, optional): True if willing to try to unblock channel.
        Defaults to True.
        pin (list, optional): list of ints with pin (Ex: [1,1,1,1]). Defaults to None.

    Raises:
        ValueError: NOT_IN_SCREEN
    """

    if page_home.go_to_home():
        stbt.press_and_wait(
            RCU.MENU.value,
            region=stbt.Region(310, 645, width=60, height=70),
            stable_secs=0.5,
        )
        _check_live_state(unblock, pin)


def get_channel_number():
    """Returns channel number from miniguide if OCR has succeeded

    Returns:
        int: channel number
    """
    return page_guia.open_guide_get_channel_number()


def assert_motion():
    return stbt.wait_for_motion(
        timeout_secs=10,
        consecutive_frames=None,
        noise_threshold=None,
        mask=MOTION_MASK,
        frames=None,
    )


def _check_live_state(unblock, pin):
    try:
        assert_screen()
    except NameError:
        if _is_channel_bocked() and unblock is True:
            stbt.draw_text("Channel is blocked")
            if not _unblock_channel(pin):
                raise NotInScreen(__name__)
            assert_screen()

        elif _is_channel_bocked() and unblock is False:
            stbt.draw_text("Channel is blocked")
            stbt.press_and_wait(RCU.EXIT.value)
            assert_screen()

        else:
            raise NotInScreen(__name__)


def _is_channel_bocked():
    return True if page_pin.is_visible() else False


def _unblock_channel(pin=None):
    page_pin.insert_pin(pin)
    return not page_pin.is_pin_incorrect()


def _convert_ch_list(ch_list):
    key = "NUMERIC_"
    return [RCU[key + str(digit)].value for digit in ch_list]
