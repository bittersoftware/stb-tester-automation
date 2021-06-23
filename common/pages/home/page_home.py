import time
import logging

import stbt
from common.utils.rcu import RCU
from common.exceptions import NotInScreen

logger = logging.getLogger(__file__)


class Img:
    """List of reference images locators"""

    LOGO = "./images/movistar_logo_transparent.png"
    DOTS = "./images/dots.png"


# Images for menu were cropped in Region(20, 372, width=243, height=57)
MENU = {
    "SEARCH": "./images/home_busqueda.png",
    "GUIA": "./images/home_guia.png",
    "U7D": "./images/home_u7d.png",
    "ORIGINALES": "./images/home_originales.png",
    "CINE": "./images/home_cine.png",
    "SERIES": "./images/home_series.png",
    "DEPORTES": "./images/home_deportes.png",
    "NETFLIX": "./images/home_netflix.png",
    "INFANTIL": "./images/home_infantil.png",
    "DOCUMENTALES": "./images/home_documentales.png",
    "MUSICA": "./images/home_musica.png",
    "OTROS": "./images/home_otros.png",
    "5S": "./images/home_5s.png",
    "ADULTOS": "./images/home_adultos.png",
    "MICUENTA": "./images/home_micuenta.png",
    "AJUSTES": "./images/home_ajustes.png",
    "APPS": "./images/home_apps.png",
}


class Home(stbt.FrameObject):
    """Page Object for Home

    When instantiated, an image capture is done and
    de property is_visible is set to True if we are
    in Home page.
    """

    def __bool__(self):
        return self.is_visible

    def __repr__(self):
        if self.is_visible:
            return "Home(is_visible=True)"
        else:
            return "Home(is_visible=False)"

    @property
    def is_visible(self):
        """Returns True if in Home page"""
        logo_img = Img.LOGO
        dots_img = Img.DOTS

        logo = stbt.match(
            logo_img,
            frame=self._frame,
            region=stbt.Region(58, 25, width=120, height=70),
        )

        dots = stbt.match(
            dots_img,
            frame=self._frame,
            region=stbt.Region(0, 478, width=158, height=138),
        )

        return logo and dots


def is_visible():
    """Check if in Home

    Returns:
        [boolean]: [Returns True if in Home]
    """
    menu = Home()
    return menu.is_visible


def assert_screen():
    """Raises Exception if not in Home

    Returns:
        [obj]: [Returns instance of page]
    """
    if is_visible():
        page = Home()
        return page
    else:
        raise NotInScreen(__name__)


def go_to_home():
    """Navigate to home if accessible by only clicking Menu button

    Returns:
        [boolean]: [Returns True if in Home]
    """

    try:
        assert_screen()
    except NotInScreen:
        stbt.press_and_wait(RCU.MENU, timeout_secs=5, stable_secs=2)
        return assert_screen()
    else:
        return True


def access_menu(item):
    """Access Home item from the ones defined in MENU dictionary

    Args:
        item ([string]): [key from MENU dictionary]
    """
    assert_screen()

    try:
        stbt.draw_text("Navigating to {}".format(item))
        stbt.press_until_match(
            RCU.LEFT,
            MENU[item],
            interval_secs=0.8,
            max_presses=len(MENU),
            region=stbt.Region(10, 350, width=270, height=90),
        )
    except Exception:
        logger.error(
            "Item not found: '{}'\nCheck valid values in MENU dictionary in {}".format(
                item, __name__
            )
        )
    else:
        time.sleep(1)
        stbt.press_and_wait(RCU.OK)
