# -*- coding: utf-8 -*-
import stbt
import time
from common.utils.rcu import RCU
from common.pages.en_vivo import page_en_vivo


def test_main():
    """Zapping 10s"""

    zap_count = 0

    # 1. Go to live
    page_en_vivo.go_to_live()
    # 2. Get start time
    start = time.time()

    while (time.time() - start) / 3600 < 6:
        # 4. Zap to channel
        time.sleep(10)
        # 3. Zap to channel
        stbt.press(RCU.CHANNELUP)
        zap_count = zap_count + 1
        stbt.draw_text("{}".format(zap_count))

    print(zap_count)
