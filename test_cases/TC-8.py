# -*- coding: utf-8 -*-
import stbt
from common.pages.home import page_home
from common.utils.rcu import RCU
from common.pages.apps import page_apps
from common.pages.apps.page_apps import App
from common.la.atleti import page_atleti
from common.la.atleti.page_atleti import Img
from utils.imports_utils import network_module, plot


def test_main():
    """Validates ABR from video stream"""

    # Live VoD Capture config
    vod_config = {
        "filter": "tcp port 80",
        "resolution": ["360", "720", "1080", "2160"],
        "eth_interface": "enp0s31f6",
    }

    # Plot VoD config
    plot_config = {
        "ylimitMax": 1200,
    }

    # Initialize Vod Cap
    network = network_module()
    capture_handler = network.NetworkCaptureHandler(vod_config)

    plt = plot()

    # Open LA
    page_home.go_to_home()
    page_home.access_menu("APPS")
    page_apps.navigate_to_app(App.ATLETI)
    stbt.press(RCU.OK)

    # Assert initial screen
    assert page_atleti.get_initial_screen()

    # Selects pill
    page_atleti.select_pill(Img.PILL_ENTREVISTA)
    stbt.press("KEY_OK")

    # Start VoD Capture
    capture_handler.start_vod_capture()

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
            page_atleti.detected_movement()

    # Wait end of video
    page_atleti.wait_end_of_video()

    # Stop VOD capture
    vod_cap_data = capture_handler.stop_vod_capture()
    print(vod_cap_data)

    # Exit screen
    stbt.press_and_wait("KEY_EXIT", stable_secs=1)

    # Create Vod Chart
    plt.CreateVodChart(plot_config, vod_cap_data)
