# -*- coding: utf-8 -*-
import stbt
from common.pages.home import page_home
from common.utils.rcu import RCU
from common.pages.apps import page_apps
from common.pages.apps.page_apps import App
from common.la.covid import page_covid


def test_main():
    """Reply all questions with Yes to confirm positive result"""

    # Answers (1 for yes, 0 for no)
    ans = [1, 1, 1, 1, 1, 1, 1, 1]

    # Open Livin App
    page_home.go_to_home()
    page_home.access_menu("APPS")
    page_apps.navigate_to_app(App.COVID)
    stbt.press(RCU.OK)

    # 1. Assert initial screen
    assert page_covid.get_initial_screen()

    # 2. Select Empezar
    page_covid.select_pill(u"Empezar")

    # 3. Reply all questions with array of answers
    page_covid.answer_all_questions(ans)

    # 4. Assert positive result
    page_covid.assert_positive_diagnosis()

    # 5. Select Salir
    page_covid.select_pill(u"Salir")
