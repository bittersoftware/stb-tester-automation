import time

import stbt

from common.pages.home import page_home
from common.pages.guia import page_guia
from common.utils import get_time_and_date as gt
from common.utils.rcu import RCU


def get_time_and_date():
    """Get Time and Date from EPG (Guide)

    Returns:
        [tuple]: (day: int, month: str, hour: int, minute: int)
    """
    page_home.go_to_home()
    page_home.access_menu("GUIA")
    return page_guia.get_time_and_date()


def assert_time():
    """Check if displayed time is correct

    Returns:
        bool: True if time matches
    """
    time = get_time_and_date()
    return gt.assert_current_time_and_date(time)


def send_num_rcu_keys(num_key_list):
    """Send sequence of numerical keys from RCU
    Expects list of ints from 0-9.

    Args:
        num_key_list (list): list of ints
    """
    assert isinstance(num_key_list, list)

    assert all(
        isinstance(digit, int) for digit in num_key_list
    ), "All digits must be integers"

    assert all(
        0 <= digit <= 9 for digit in num_key_list
    ), "All digits must be in range 0-9"

    rcu = vars(RCU)
    converted_digit_list = [rcu["NUMERIC_" + str(digit)] for digit in num_key_list]

    for index, digit in enumerate(converted_digit_list):
        stbt.press(digit)
        time.sleep(0.5)
