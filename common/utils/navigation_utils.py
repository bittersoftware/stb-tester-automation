from common.pages.home import page_home
from common.pages.guia import page_guia
from common.utils import get_time_and_date as gt


def get_time_and_date():
    page_home.go_to_home()
    page_home.access_menu("GUIA")
    return page_guia.get_time_and_date()


def assert_time():
    time = get_time_and_date()
    return gt.assert_current_time_and_date(time)
