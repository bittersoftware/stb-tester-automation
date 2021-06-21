# -*- coding: utf-8 -*-
import re

import stbt
from common.exceptions import Error, NotInScreen, NotFound, ArgumentNotValid
from common.utils.rcu import RCU


class Img:
    """List of reference images locators"""

    LOGO = "./images/covid_gobierno_logo.png"
    PILL_LEFT = "./images/covid_pill_left.png"
    PILL_RIGHT = "./images/covid_pill_right.png"
    SI_OPT = "./images/covid_si.png"
    NO_OPT = "./images/covid_no.png"
    SCREEN_INITIAL = "./images/covid_initial.png"
    SCREEN_SPLASH = "./images/covid_splash.png"
    NEGATIVE_RESULT = "./images/covid_resultado_negativo.png"
    POSITIVE_RESULT = "./images/covid_resultado_positivo.png"


class Covid(stbt.FrameObject):
    """Page Object for Covid

    When instantiated, an image capture is done and
    de property is_visible is set to True if we are
    in Covid page.
    """

    def __bool__(self):
        return self.is_visible

    def __repr__(self):
        if self.is_visible:
            return "Covid(is_visible=True)"
        else:
            return "Covid(is_visible=False)"

    @property
    def is_visible(self):
        """Returns True if in Covid page"""

        region = stbt.Region(85, 30, width=180, height=100)

        logo = stbt.match(Img.LOGO, frame=self._frame, region=region)

        return logo

    @property
    def focused_pill(self):
        """Returns ascii string for focused pills
        Does not consider as pill the options SI/NO of the questions asked

        Since pills vary in horizontal size, we detect left and right edges,
        then make a bounding_box to get the pill region and perform OCR

        Returns:
            string: Focused text in ascii. No special characters. None if no pill
        """
        region = stbt.Region(0, 510, width=1280, height=185)

        pill_left = stbt.match(
            Img.PILL_LEFT,
            frame=self._frame,
            region=region,
        )

        pill_right = stbt.match(
            Img.PILL_RIGHT,
            frame=self._frame,
            region=region,
        )

        if not pill_right.match and not pill_left.match:
            return None

        pill_region = stbt.Region.bounding_box(pill_left.region, pill_right.region)

        # For some reason, tesseract does not read well when there is only one word
        # in this capture
        # Cropped pill_region in order to have single color background instead of
        # showing the pills' borders.

        pill_croped = pill_region.extend(x=24, y=6, right=-25, bottom=-6)

        return stbt.ocr(
            frame=self._frame,
            region=pill_croped,
            lang="spa",
            mode=stbt.OcrMode.SINGLE_LINE,
        )

    @property
    def current_question_number(self):
        """Returns OCR number from question
        Data properly treated in get_current_question_number function

        Returns:
            string: raw string with number
        """
        region = stbt.Region(110, 200, width=50, height=40)

        return stbt.ocr(frame=self._frame, region=region, mode=stbt.OcrMode.RAW_LINE)


def is_visible():
    """Check if in Covid

    Returns:
        [boolean]: [Returns True if in Covid]
    """
    page = Covid()
    return page.is_visible


def assert_screen():
    """Raises Exception if not in Covid

    Returns:
        [obj]: [Returns instance of page]
    """
    if is_visible():
        page = Covid()
        return page
    else:
        raise NotInScreen(__name__)


def get_focused_pill():
    """Get focused pill text in unicode format

    Returns:
        unicode: text from focused pill
    """

    page = assert_screen()
    try:
        focused = page.focused_pill
    except AttributeError:
        return None
    else:
        return focused


def get_current_question_number():
    """Returns number of the current question.

    Returns:
        int: number of current question if found or None otherwise.
    """
    page = assert_screen()
    num_raw = page.current_question_number
    try:
        num = re.findall(r"\d{1}", num_raw)[0]
        num = int(num)
    except ValueError:
        return None
    else:
        stbt.draw_text("Question: {}".format(str(num)))
        return num


def get_splash_screen():
    """Wait for the splash screen to appear.

    Returns:
        boolean: returns True if the splash screen was found within 15 seconds
    """
    try:
        stbt.wait_for_match(Img.SCREEN_SPLASH, timeout_secs=15)
    except stbt.MatchTimeout:
        return False
    else:
        return True


def get_initial_screen():
    """Wait for the initial screen to appear.

    Returns:
        boolean: returns True if the initial screen was found within 30 seconds
    """
    try:
        stbt.wait_for_match(Img.SCREEN_INITIAL, timeout_secs=30)
    except stbt.MatchTimeout:
        return False
    else:

        return True


def select_pill(unicode_text, press_ok=True):
    """Select pill by sending an unicode text as argument.

    Args:
        unicode_text (unicode): unicode text of the pill to select.
        press_ok (bool, optional): press ok when pill is found. Defaults to True.

    Raises:
        exceptions.ArgumentNotValid: if argument is not in unicode.
        exceptions.NotInScreen: if not in this page object screen is selected
        exceptions.NotFound: if item was not found.
    """
    if not isinstance(unicode_text, unicode):
        raise ArgumentNotValid

    page = assert_screen()
    focused = get_focused_pill().lower()

    if focused is None:
        raise NotInScreen(__name__)

    unicode_text = unicode_text.lower()

    for _ in range(6):
        if unicode_text == focused:
            stbt.draw_text(
                "Pill found: {}".format(
                    unicode_text.encode("ascii", "ignore").decode("ascii")
                )
            )

            if press_ok:
                stbt.press_and_wait(RCU.OK, stable_secs=0.5)
                return
            else:
                return
        else:
            stbt.press_and_wait(RCU.RIGHT, stable_secs=0.5)

        page.refresh()
        focused = get_focused_pill().lower()

    stbt.draw_text(
        "Pill Not Found: {}".format(
            unicode_text.encode("ascii", "ignore").decode("ascii")
        )
    )
    raise NotFound()


def select_option_yes():
    """Select option YES as answer"""
    stbt.press_until_match(
        RCU.RIGHT,
        Img.SI_OPT,
        interval_secs=0.5,
        max_presses=3,
        region=stbt.Region(125, 420, width=330, height=80),
    )
    stbt.draw_text("Select option: YES")
    stbt.press_and_wait(RCU.OK, stable_secs=0.5)


def select_option_no():
    """Select option NO as answer"""
    stbt.press_until_match(
        RCU.RIGHT,
        Img.NO_OPT,
        interval_secs=0.5,
        max_presses=3,
        region=stbt.Region(125, 420, width=330, height=80),
    )
    stbt.draw_text("Select option: NO")
    stbt.press_and_wait(RCU.OK, stable_secs=0.5)


def answer_all_questions(answers):
    """Reply all questions by sending an array of answers

    Args:
        answers (list): list of integers with 0 for NO and 1 for YES

    Raises:
        exceptions.ArgumentNotValid: if any item is not 1 or 0
        exceptions.ArgumentNotValid: if number of answers is different from 80
        exceptions.Error: If current number of screen is different from expected
    """
    NUMBER_OF_QUESTIONS = 8
    page = assert_screen()

    if not all(v == 0 or v == 1 for v in answers):
        raise ArgumentNotValid

    if not len(answers) == NUMBER_OF_QUESTIONS:
        raise ArgumentNotValid

    for question, answer in enumerate(answers, start=1):
        if answer == 0:
            select_option_no()
        else:
            select_option_yes()

        question += 1
        page.refresh()

        if (
            question <= NUMBER_OF_QUESTIONS
            and question != get_current_question_number()
        ):
            raise Error("Mismatch between current/expected question number")


def assert_negative_diagnosis():
    """Detect screen for negative diagnosis"""
    assert_screen()
    assert stbt.wait_until(
        lambda: stbt.match(
            Img.NEGATIVE_RESULT,
            region=stbt.Region(95, 110, width=590, height=190),
        )
    )


def assert_positive_diagnosis():
    """Detect screen for positive diagnosis"""
    assert_screen()
    assert stbt.wait_until(
        lambda: stbt.match(
            Img.POSITIVE_RESULT,
            region=stbt.Region(95, 110, width=590, height=190),
        )
    )
