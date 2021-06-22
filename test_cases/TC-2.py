# -*- coding: utf-8 -*-
from common.pages.pin import page_pin
from common.pages.en_vivo import page_en_vivo


def test_main():
    """Unblock channel."""

    CHANNEL = 4

    # 1. Zap to channel
    page_en_vivo.zap_to_ch(CHANNEL, unblock=False)
    # 2. Confirm is blocked
    assert page_pin.is_visible()
    # 3. Insert PIN
    page_pin.insert_pin()
    # 4. Confirm channel is unblocked - motion
    assert page_en_vivo.assert_motion()
