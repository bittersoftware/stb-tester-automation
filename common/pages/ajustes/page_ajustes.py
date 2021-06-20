# -*- coding: utf-8 -*-
import time

import numpy as np
import stbt
from common.exceptions import NotInScreen, NotFound
from common.utils.get_time_and_date import GetTimeAndDate
from common.utils.rcu import RCU

# Lists to compose 2d matrix for Ajustes options
AJUSTES_R1 = ["Modo de pantalla", "Dolby Audio", "Lanzar y ver", "Control parental"]
AJUSTES_R2 = ["Bloqueo de canales", "PIN de compra", "PIN parental", "Ver mensajes"]
AJUSTES_R3 = ["Mensajes", "Espacio Libre", "Gestión de series", "Conoce M+"]
AJUSTES_R4 = ["Modos de apagado", "Netflix"]

# Create 2d matrix to correspond to the current menu in Ajustes page
AJUSTES = []
AJUSTES.append(AJUSTES_R1)
AJUSTES.append(AJUSTES_R2)
AJUSTES.append(AJUSTES_R3)
AJUSTES.append(AJUSTES_R4)


class Img():
    """List of reference images locators
    """

    LOGO = "./images/ajustes_logo.png"
    SELECTED = "./images/ajustes_selection.png"


class Ajustes(stbt.FrameObject):
    """Page Object for Ajustes

    When instantiated, an image capture is done and
    de property is_visible is set to True if we are
    in Ajustes page.
    """

    def __bool__(self):
        return self.is_visible

    def __repr__(self):
        if self.is_visible:
            return "Ajustes(is_visible=True)"
        else:
            return "Ajustes(is_visible=False)"

    @property
    def is_visible(self):
        """Returns True if in Ajustes page"""
        logo_img = Img.LOGO
        select_img = Img.SELECTED

        logo = stbt.match(
            logo_img,
            frame=self._frame,
            match_parameters=None,
            region=stbt.Region(1125, 25, width=115, height=65),
        )

        selection = stbt.match(select_img, frame=self._frame, match_parameters=None)

        return logo and selection


def is_visible():
    """Check if in Ajustes

    Returns:
        [boolean]: [Returns True if in Ajustes]
    """
    ajustes = Ajustes()
    return ajustes.is_visible


def assert_screen():
    """Raises Exception if not in BlockChannels

    Returns:
        [obj]: [Returns instance of page]
    """
    if is_visible():
        page = Ajustes()
        return page
    else:
        raise NotInScreen(__name__)


def access_ajustes(item):
    """Access Ajustes item from the ones defined in AJUSTES 2d matrix
       Finds current selected element indexes
       Finds target element indexes
       Subtract both elements to find needed RCU commands to reach target

    Args:
        item ([string]): [key from AJUSTES 2d matrix]
    """
    if is_visible():
        selected_item = selected()
        stbt.draw_text("Navigating to {} from {}".format(item, selected_item))
        selected_index = _aux_index_2d(selected_item)
        target_index = _aux_index_2d(item)
        directions = np.subtract(target_index, selected_index)
        print(directions)
        vertical = directions[0]
        horizontal = directions[1]

        _matrix_nav(horizontal, vertical)

        time.sleep(1)
        if selected() == item:
            stbt.press_and_wait(
                RCU.OK,
                region=stbt.Region.ALL,
                timeout_secs=3,
                stable_secs=1,
            )
        else:
            stbt.draw_text("Could not reach element")
            raise NotFound()


def selected():
    select_img = Img.SELECTED
    selection = stbt.match(select_img, match_parameters=None)
    return stbt.ocr(
        region=selection.region,
        text_color=(255, 249, 182),
        text_color_threshold=80,
        mode=stbt.OcrMode.SPARSE_TEXT_WITH_OSD,
        lang="spa",
    )


def get_time_and_date():
    """Returns date and time Ajustes and sub-menu screens

    Returns:
        [tuple]: (day: int, month: str, hour: int, minute: int)
    """
    screen = assert_screen()
    t = GetTimeAndDate(screen)
    return t.time_and_date_parsed


def _aux_index_2d(item):
    for i, e in enumerate(AJUSTES):
        try:
            return i, e.index(item)
        except ValueError:
            pass
    print("Element not foun: {}".format(item))
    print(
        "Item not found: '{}'\nCheck valid values in MENU dictionary in {}".format(
            item, __name__
        )
    )


def _matrix_nav(horizontal, vertical):
    if vertical > 0:
        for _ in range(vertical):
            stbt.press(RCU.DOWN)
    else:
        for _ in range(abs(vertical)):
            stbt.press(RCU.UP)

    if horizontal > 0:
        for _ in range(horizontal):
            stbt.press(RCU.RIGHT)
    else:
        for _ in range(abs(horizontal)):
            stbt.press(RCU.LEFT)
