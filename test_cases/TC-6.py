# -*- coding: utf-8 -*-
import stbt
import time
import json
from common.pages.home import page_home
from common.utils.rcu import RCU
from common.pages.apps import page_apps
from common.pages.apps.page_apps import App
from common.la.atleti import page_atleti
from utils.imports_utils import plot


def test_main():
    """KPI for opening Living App: Atletico de Madrid"""

    # Stores kpi timing
    kpi = []

    # repetition times
    repeat = 15

    for i in range(repeat):
        # Open LA
        page_home.go_to_home()
        page_home.access_menu("APPS")
        page_apps.navigate_to_app(App.ATLETI)
        stbt.press(RCU.OK.value)

        # Calculates time until initial screen
        start = time.time()
        assert page_atleti.get_initial_screen()
        end = time.time()
        kpi.append(end - start)

        # Log info in screen
        stbt.draw_text("Execution {} of {}".format(i + 1, repeat))
        stbt.draw_text("Opened  in  {}s".format(round(end - start, 2)))

    # store values in file
    with open("timings_demo.json", "w") as f:
        json.dump({"app_access_time": kpi}, f)

    print("Max Time: {}".format(max(kpi)))
    print("Min Time: {}".format(min(kpi)))
    print("Avg Time: {}".format(sum(kpi) / len(kpi)))

    # Plots bar chart
    p = plot()
    p.PlotBarChart(kpi, treshold=7, title="KPI - Access", fname="image")
