# -*- coding: utf-8 -*-
import stbt
import time
import json
from common.utils.plot import PlotBarChart
from common.pages.ajustes import page_ajustes
from common.pages.pin import page_pin
from common.pages.home import page_home
from common.pages.guia import page_guia
from common.pages.bloqueo_de_canales import page_bloqueo_de_canales
from common.utils.rcu import RCU
from common.pages.en_vivo import page_en_vivo
from common.pages.apps import page_apps
from common.pages.apps.page_apps import App
from common.la.covid import page_covid


def test_main():
    page_home.go_to_home()
    page_home.access_menu("AJUSTES")
    page_ajustes.access_ajustes("Bloqueo de canales")
    page_pin.insert_pin()
    page_bloqueo_de_canales.navigate_to_channel(2)
    page_bloqueo_de_canales.block_channel()
    page_bloqueo_de_canales.confirm_changes_popup()
    page_en_vivo.go_to_live()
    page_en_vivo.zap_to_ch(2, unblock=False)
    assert page_pin.is_visible()


def test_main2():
    kpi = []
    for _ in range(50):
        page_home.go_to_home()
        page_home.access_menu("APPS")
        page_apps.navigate_to_app(App.COVID)
        stbt.press(RCU.OK)
        start = time.time()
        assert page_covid.get_initial_screen()
        end = time.time()
        kpi.append(end - start)
        stbt.draw_text("Opened  in  {}s".format(round(end - start, 2)))

    with open("timings_demo.json", "w") as f:
        json.dump({"app_access_time": kpi}, f)

    PlotBarChart(kpi, treshold=10)


def test_main3():
    a = page_guia.get_parental()
    b = page_guia.get_hd()
    c = page_guia.get_dolby()
    d = page_guia.get_event_title()
    e = page_guia.get_exihbition_times()
    f = page_guia.get_channel_number()

    print(a, b, c, e, f)
    print(d)
    time.sleep(4)


def text_match_assistent(ocr, ref):
    print(ocr.lower(), ref.lower())
    return ref.lower() in ocr.lower()


timing = []
