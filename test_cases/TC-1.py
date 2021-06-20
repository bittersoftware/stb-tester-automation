# -*- coding: utf-8 -*-
from common.pages.ajustes import page_ajustes
from common.pages.pin import page_pin
from common.pages.home import page_home
from common.pages.bloqueo_de_canales import page_bloqueo_de_canales
from common.pages.en_vivo import page_en_vivo


def test_main():
    """Block channel and assert it is blocked."""

    CHANNEL = 4

    # 1. Open  home
    page_home.go_to_home()
    # 2. Navigate to ajustes
    page_home.access_menu("AJUSTES")
    # 3. Navigate to Bloqueo de canales
    page_ajustes.access_ajustes("Bloqueo de canales")
    # 4. Insert pin
    page_pin.insert_pin()
    # 5. Navigate to desired channel
    page_bloqueo_de_canales.navigate_to_channel(CHANNEL)
    # 6. Block desired channel
    page_bloqueo_de_canales.block_channel()
    # 7. Save changes
    page_bloqueo_de_canales.confirm_changes_popup()
    # 8. Go to live
    page_en_vivo.go_to_live()
    # 9. Zap to channel
    page_en_vivo.zap_to_ch(CHANNEL, unblock=False)
    # 10. Confirm is blocked
    assert page_pin.is_visible()
