# -*- coding: utf-8 -*-
import time

import stbt
from common.exceptions import NotInScreen, TimeoutError
from common.utils.rcu import RCU


class Img:
    """List of reference images locators"""

    SCREEN_SPLASH = "./images/atleti_splash_screen.png"
    SCREEN_INITIAL = "./images/atleti_initial_screen.png"
    LOGO = "./images/atleti_logo.png"
    LEFT_ICON = "./images/atleti_left_icon.png"
    RIGHT_ICON = "./images/atleti_right_icon.png"
    PILL_SIDE = "./images/atleti_pill.png"
    PILL_RESUMEN = "./images/atleti_pill_resumen.png"
    PILL_ATLETICO = "./images/atleti_pill_atletico.png"
    PILL_ENTREVISTA = "./images/atleti_pill_entrevista.png"
    PILL_PROTAGONISTA = "./images/atleti_pill_protagonista.png"
    CONTINUAR = "./images/atleti_dialog_continuar.png"
    PILL_REPRODUCIR_DEL_INICIO = (
        "./images/atleti_pill_reproducir_desde_el_principio.png"
    )
    PILL_CONTINUAR = "./images/atleti_pill_continuar.png"
    PLAYER_PAUSE_ICON = "./images/atleti_player_pause_icon.png"
    PLAYER_RESTART_ICON = "./images/atleti_player_restart_icon.png"
    PLAYER_MASK = "./images/atleti_player_mask.png"
    TILE_SELECTED = "./images/atleti_tile_selected.png"


class Atleti(stbt.FrameObject):
    """Page Object for Atleti

    When instantiated, an image capture is done and
    de property is_visible is set to True if we are
    in Atleti page.
    """

    def __bool__(self):
        return self.is_visible

    def __repr__(self):
        if self.is_visible:
            return "Atleti(is_visible=True)"
        else:
            return "Atleti(is_visible=False)"

    @property
    def is_visible(self):
        """Returns True if in Atleti page"""

        region = stbt.Region(95, 35, width=135, height=100)

        logo = stbt.match(
            Img.LOGO, frame=self._frame, match_parameters=None, region=region
        )

        return logo

    @property
    def is_pill_selected(self):
        """Returns ascii string for focused pills
        Does not consider as pill the options SI/NO of the questions asked

        Returns:
            string: Focused text in ascii. No special characters. None if no pill
        """
        region = stbt.Region(80, 595, width=1170, height=65)

        pills = [
            Img.PILL_RESUMEN,
            Img.PILL_ENTREVISTA,
            Img.PILL_PROTAGONISTA,
            Img.PILL_ATLETICO,
        ]

        for pill in pills:
            if stbt.match(
                pill, frame=self._frame, match_parameters=None, region=region
            ):
                return pill.name

        return False


def is_visible():
    """Check if in Atleti

    Returns:
        [boolean]: [Returns True if in Atleti]
    """
    page = Atleti()
    return page.is_visible


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


def assert_screen():
    """Raises Exception if not in Atleti

    Returns:
        [obj]: [Returns instance of page]
    """
    if is_visible():
        page = Atleti()
        return page
    else:
        raise NotInScreen(__name__)


def get_selected_pill():
    page = assert_screen()
    return page.is_pill_selected


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


def select_pill(pill, change_dir=False):
    """Navigate right until find target pill

    Args:
        pill ([Enum]): [Img.PILL_RESUMEN, Img.PILL_ENTREVISTA,
        Img.PILL_PROTAGONISTA, Img.PILL_ATLETIOO]
    """
    if change_dir:
        stbt.press_until_match(
            RCU.LEFT,
            pill,
            max_presses=4,
            interval_secs=0.8,
            region=stbt.Region(80, 595, width=1170, height=65),
        )
    else:
        try:
            stbt.press_until_match(
                RCU.RIGHT,
                pill,
                max_presses=4,
                interval_secs=0.8,
                region=stbt.Region(80, 595, width=1170, height=65),
            )
        except stbt.MatchTimeout:
            select_pill(pill, change_dir=True)


def is_continue_popup():
    """Detects if resume dialog is opened

    Returns:
        bool: True if detected, else False
    """
    return stbt.match(
        Img.CONTINUAR,
        match_parameters=None,
        region=stbt.Region(260, 165, width=755, height=220),
    )


def select_continue():
    """Select Continue"""
    stbt.press_until_match(
        RCU.LEFT,
        Img.PILL_CONTINUAR,
        max_presses=2,
        interval_secs=0.8,
        region=stbt.Region(318, 370, width=645, height=70),
    )


def select_start_over():
    """Select Reproducir desde el principio"""
    stbt.press_until_match(
        RCU.RIGHT,
        Img.PILL_REPRODUCIR_DEL_INICIO,
        max_presses=2,
        interval_secs=0.8,
        region=stbt.Region(318, 370, width=645, height=70),
    )


def detected_movement():
    """Detects motion when in player position

    Returns:
        bool: True if motion is detected, else False
    """
    try:
        stbt.wait_for_motion(timeout_secs=20, mask=Img.PLAYER_MASK)
        return True
    except stbt.MotionTimeout:
        return False


def wait_end_of_video(timeout_secs=120, pool_interval=3):
    start_time = time.time()

    while time.time() - start_time < timeout_secs:
        first_frame = stbt.get_frame()
        time.sleep(pool_interval)
        if stbt.match(first_frame):
            return
    raise TimeoutError
