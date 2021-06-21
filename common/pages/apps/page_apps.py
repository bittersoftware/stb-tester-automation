# -*- coding: utf-8 -*-
import stbt
from common.exceptions import NotInScreen
from common.utils.rcu import RCU


# Relative path for images from ajustes
class Img:
    IMAGES_DIR = "./images/apps_"
    SELECTION = IMAGES_DIR + "selection.png"


class App:
    COVID = "./images/apps_covid.png"
    ATLETI = "./images/apps_atleti.png"


class Category:
    COMPRAS = "Compras"
    DESTACADOS = "Destacados"
    ZONA_MOVISTAR = "Zona_Movistar"
    OCIO_Y_ENTRETENIMIENTO = "Ocio y entretenimiento"
    ESTILO_DE_VIDA = "Estilo de vida"
    EDUCACION_Y_CULTURA = "Educacin y cultura"
    EMPRENDEDORES = "Emprendedores"


class Apps(stbt.FrameObject):
    """Page Object for Apps

    When instantiated, an image capture is done and
    de property is_visible is set to True if we are
    in Apps page.
    """

    def __bool__(self):
        return self.is_visible

    def __repr__(self):
        if self.is_visible:
            return "Apps(is_visible=True)"
        else:
            return "Apps(is_visible=False)"

    @property
    def is_visible(self):
        """Returns True if in Apps page"""

        region1 = stbt.Region(65, 40, width=95, height=40)
        region2 = stbt.Region(80, 375, width=285, height=175)

        apps_text = stbt.match_text(
            "Apps", frame=self._frame, region=region1, mode=stbt.OcrMode.SINGLE_WORD
        ).match

        match_parameters = stbt.MatchParameters(confirm_method=None)

        selection = stbt.match(
            Img.SELECTION,
            frame=self._frame,
            match_parameters=match_parameters,
            region=region2,
        )

        return apps_text and selection

    @property
    def category(self):
        return stbt.ocr(
            frame=self._frame,
            region=stbt.Region(85, 335, width=320, height=45),
            lang="spa",
            mode=stbt.OcrMode.SPARSE_TEXT_WITH_OSD,
        )

    @property
    def current_selected_in_category(self):
        current = stbt.ocr(
            frame=self._frame,
            region=stbt.Region(1123, 350, width=19, height=18),
            mode=stbt.OcrMode.RAW_LINE,
        )

        try:
            current = int(current)
        except ValueError:
            return None
        else:
            return current

    @property
    def total_in_category(self):
        total = stbt.ocr(
            frame=self._frame,
            region=stbt.Region(1171, 350, width=19, height=18),
            mode=stbt.OcrMode.RAW_LINE,
        )

        try:
            total = int(total)
        except ValueError:
            return None
        else:
            return total


def is_visible():
    """Check if in Apps

    Returns:
        [boolean]: [Returns True if in Apps]
    """
    apps = Apps()
    return apps.is_visible


def assert_screen():
    """Raises Exception if not in Apps

    Returns:
        [obj]: [Returns instance of page]
    """
    if is_visible():
        page = Apps()
        return page
    else:
        raise NotInScreen(__name__)


def get_category():
    page = assert_screen()
    return page.category.encode("ascii", "ignore").decode("ascii")


def get_current_selected_in_category():
    page = assert_screen()
    return page.current_selected_in_category


def get_total_in_category():
    page = assert_screen()
    return page.total_in_category


def navigate_to_category(category):
    # Type checking
    if not isinstance(category, Category):
        raise TypeError("category must be an instance of Category Enum")

    assert_screen()

    if not get_category() == category:
        for _ in range(len(Category)):
            stbt.press_and_wait(RCU.DOWN, stable_secs=0.5)
            if get_category() == category:
                return True
        return False

    return True


def navigate_to_app(app):
    # Type checking
    if not isinstance(app, App):
        raise TypeError("app must be an instance of App Enum")

    assert_screen()

    stbt.press_until_match(
        RCU.RIGHT,
        app,
        interval_secs=0.8,
        region=stbt.Region(80, 375, width=285, height=175),
    )
