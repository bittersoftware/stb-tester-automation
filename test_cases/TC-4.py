# -*- coding: utf-8 -*-
import stbt
import json
from common.pages.home import page_home
from common.utils.rcu import RCU
from common.pages.apps import page_apps
from common.pages.apps.page_apps import App
from common.la.covid import page_covid
from collections import Counter


def test_main():
    """Splash Screen: Asistente COVID"""

    # Stores kpi timing
    splash = []

    # repetition times
    repeat = 20

    for i in range(repeat):
        # Open Living App
        page_home.go_to_home()
        page_home.access_menu("APPS")
        page_apps.navigate_to_app(App.COVID)
        stbt.press(RCU.OK)

        # Confirms that splash screen was displayed
        try:
            assert page_covid.get_splash_screen()
        except AssertionError:
            splash.append("Not displayed")
            stbt.draw_text("Splash screen not shown")
        else:
            splash.append("Displayed")
            stbt.draw_text("Splash screen displayed")

        # Log info in screen
        stbt.draw_text("Execution {} of {}".format(i + 1, repeat))

    # store values in file
    with open("splash.json", "w") as f:
        json.dump({"splash": splash}, f)

    # Counts how incidences of splash screen displayed/not displayed
    result = dict(Counter(splash))

    print("Result: {}".format(result))
