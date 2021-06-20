# -*- coding: utf-8 -*-
import json
import time

from common.pages.guia import page_guia


def test_main():
    """EPG Metadata."""
    metadata = {}

    page_guia.open_guide()

    metadata["event_title"] = page_guia.get_event_title()
    metadata["parental_rate"] = page_guia.get_parental()
    metadata["exihbition_times"] = page_guia.get_exihbition_times()
    metadata["channel_number"] = page_guia.get_channel_number()
    metadata["hd"] = page_guia.get_hd()
    metadata["dolby"] = page_guia.get_dolby()

    time.sleep(5)

    with open("event_metadata.json", "w") as f:
        json.dump(metadata, f)
