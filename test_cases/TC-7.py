# -*- coding: utf-8 -*-
import stbt
from common.pages.home import page_home
from common.utils.rcu import RCU
from common.pages.apps import page_apps
from common.pages.apps.page_apps import App
from common.la.atleti import page_atleti
from common.la.atleti.page_atleti import Img


def test_main():
    """Validates all pills have a video stream"""

    # Open LA
    page_home.go_to_home()
    page_home.access_menu("APPS")
    page_apps.navigate_to_app(App.ATLETI)
    stbt.press(RCU.OK)

    # Assert initial screen
    assert page_atleti.get_initial_screen()

    # List of pills
    pills = [
        Img.PILL_RESUMEN,
        Img.PILL_ENTREVISTA,
        Img.PILL_PROTAGONISTA,
        Img.PILL_ATLETICO,
    ]

    # Iterate over each option
    for pill in pills:
        # Selects pill
        page_atleti.select_pill(pill)
        stbt.press("KEY_OK")
        # Check if there is movement
        if not page_atleti.detected_movement():
            # Check if is in resume popup
            if not page_atleti.is_continue_popup():
                # Fails if not movement and not in resume popup
                assert False
            else:
                # Select Start Over
                page_atleti.select_start_over()
                stbt.press("KEY_OK")
                # Confirm if video is played
                assert page_atleti.detected_movement()

        stbt.press_and_wait("KEY_EXIT", stable_secs=1)
