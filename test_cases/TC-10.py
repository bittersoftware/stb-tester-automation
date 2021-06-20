# -*- coding: utf-8 -*-
import stbt
import time
from common.utils.rcu import RCU
from common.pages.en_vivo import page_en_vivo
from utils.imports_utils import network_module, plot


def test_main():
    """Fast Channel Change capture"""

    # Live Capture config
    CHANNEL = 13

    live_config = {
        "eth_interface": "enp0s31f6",
        "udp_ports": {"multicast": "8208", "fcc": "4096", "ret": "4098"},
    }
    # Live Chart config
    chart_config = {"ylimitMax": 8400, "ylimitMin": 4000}

    net = network_module()

    # 1. Go to live
    page_en_vivo.go_to_live()
    # 2. Zap to channel
    page_en_vivo.zap_to_ch(CHANNEL, unblock=False)
    time.sleep(10)

    capture_handler = net.NetworkCaptureHandler(live_config)
    capture_handler.start_live_capture()

    time.sleep(2)

    stbt.press(RCU.CHANNELUP)

    time.sleep(10)

    data = capture_handler.stop_live_capture()

    p = plot()
    p.CreateLiveChart(chart_config, data)
