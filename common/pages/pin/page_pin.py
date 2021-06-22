# -*- coding: utf-8 -*-
import stbt
from common.utils.navigation_utils import send_num_rcu_keys
from common.exceptions import NotInScreen


class Img:
    """List of reference images locators"""

    PIN_FOCUS = "./images/pin_box_focused.png"
    PIN_NOT_FOCUS = "./images/pin_box_not_focused.png"
    PIN_RED_BOX = "./images/pin_incorrect_red_box.png"
    PIN_INCORRECT_TEXT = "./images/pin_incorrect.png"


DEFAULT_PIN = 1111


class Pin(stbt.FrameObject):
    """Page Object for Pin

    When instantiated, an image capture is done and
    de property is_visible is set to True if we are
    in Pin page.
    """

    def __bool__(self):
        return self.is_visible

    def __repr__(self):
        if self.is_visible:
            return "Pin(is_visible=True)"
        else:
            return "Pin(is_visible=False)"

    @property
    def is_visible(self):
        """Returns True if in Pin page"""

        region = stbt.Region(475, 335, width=315, height=80)

        box_1 = stbt.match(
            Img.PIN_FOCUS, frame=self._frame, region=region
        )

        box_2 = stbt.match(
            Img.PIN_NOT_FOCUS, frame=self._frame, region=region
        )

        return box_1 and box_2


def is_visible():
    """Check if in Pin

    Returns:
        [boolean]: [Returns True if in Pin]
    """
    pin = Pin()
    return pin.is_visible


def assert_screen():
    """Raises Exception if not in Pin

    Returns:
        [obj]: [Returns instance of page]
    """
    if is_visible():
        page = Pin()
        return page
    else:
        raise NotInScreen(__name__)


def insert_pin(digit_list=DEFAULT_PIN):
    """Insert PIN from 4-digit list in string format from lircd database

    Args:
        digit_list (int): Int 4 digits. Defaults to DEFAULT_PIN: 1111.
    """
    digit_list = DEFAULT_PIN if digit_list is None else digit_list

    digit_list = [int(i) for i in str(digit_list)]

    assert len(digit_list) == 4, "Invalid number of digits. Must be 4 digits"
    assert all(
        isinstance(digit, int) for digit in digit_list
    ), "All digits must be integers"
    assert all(
        0 <= digit <= 9 for digit in digit_list
    ), "All digits must be in range 0-9"

    if assert_screen():
        send_num_rcu_keys(digit_list)

        region = stbt.Region(440, 315, width=390, height=155)

        assert stbt.wait_until(
            lambda: not stbt.match(Img.PIN_FOCUS, region=region)
            and not stbt.match(Img.PIN_NOT_FOCUS, region=region)
            or stbt.match(Img.PIN_INCORRECT_TEXT, region=region),
            timeout_secs=3,
        )


def is_pin_incorrect():
    """Checks if in pin screen and "PIN INCORRECTO" string
    is displayed

    Returns:
        [boolean]: [True if pin is incorrect]
    """
    txt_region = stbt.Region(530, 425, width=225, height=40)
    pin_incorrect_text = stbt.ocr(
        region=txt_region,
        text_color_threshold=80,
        mode=stbt.OcrMode.SPARSE_TEXT_WITH_OSD,
        lang="spa",
    )

    if is_visible() and pin_incorrect_text == "PIN INCORRECTO":
        stbt.draw_text("PIN INCORRECTO")
        return True
    else:
        stbt.draw_text("PIN CORRECTO")
        return False
