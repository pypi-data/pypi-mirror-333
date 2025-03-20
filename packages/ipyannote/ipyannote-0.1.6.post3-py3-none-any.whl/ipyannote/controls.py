import anywidget
from ipywidgets import jslink
from traitlets import Bool, Float
from pathlib import Path


class Controls(anywidget.AnyWidget):
    _esm = Path(__file__).parent / "static" / "controls.js"
    _css = Path(__file__).parent / "static" / "controls.css"

    current_time = Float(0.0).tag(sync=True)
    playing = Bool(False).tag(sync=True)

    def sync(self, waveform: "Waveform"): # type: ignore
        keys = ["playing", "current_time"]
        unlinks = {key: jslink((self, key), (waveform, key)).unlink for key in keys}

        def unlink():
            for unlink in unlinks.values():
                unlink()

        return unlink

