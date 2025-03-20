from typing import Optional
from pathlib import Path

import anywidget
from ipywidgets import jslink
from traitlets import Dict, Unicode, Int


class Labels(anywidget.AnyWidget):
    _esm = Path(__file__).parent / "static" / "labels.js"
    _css = Path(__file__).parent / "static" / "labels.css"

    labels = Dict(key_trait=Unicode(), value_trait=Unicode()).tag(sync=True)
    color_cycle = Int(0).tag(sync=True)
    active_label = Unicode(None, allow_none=True).tag(sync=True)

    def __init__(self, labels: Optional[dict[str, str]] = None):
        super().__init__()
        if labels:
            self.labels = labels

    def sync(self, waveform: "Labels | Waveform"):  # type: ignore
        keys = ["labels", "color_cycle", "active_label"]
        unlinks = {key: jslink((self, key), (waveform, key)).unlink for key in keys}

        def unlink():
            for unlink in unlinks.values():
                unlink()

        return unlink
