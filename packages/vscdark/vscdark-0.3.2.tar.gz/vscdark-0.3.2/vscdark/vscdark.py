from pathlib import Path

import matplotlib.pyplot as plt
from IPython.display import HTML, display

theme = "vscdark.vscdark"
theme_is_dark = True
verbose_css = False


def set_style(
    new_theme: str | None = None, dark: bool | None = None, display_css: bool = True, verbose: bool | None = None
) -> None:
    global theme
    global theme_is_dark
    global verbose_css

    theme = theme if new_theme is None else new_theme
    theme_is_dark = theme_is_dark if dark is None else dark
    verbose_css = verbose_css if verbose is None else verbose

    if theme == "vscdark":
        theme = "vscdark.vscdark"
        dark = True if dark is None else dark
    elif theme == "vsclight":
        theme = "vscdark.vsclight"
        dark = False if dark is None else dark

    plt.style.use(theme)

    if display_css:
        display(css())


def css() -> HTML:
    return HTML(
        ("Widget CSS Active" if verbose_css else "") + "<style>"
        ".cell-output-ipywidget-background {background-color: transparent !important;}"
        ".jp-OutputArea-output {background-color: transparent !important;}"
        "div.jupyter-widgets.widget-label {display: none;}"
        + (
            ".widget-label {color: white !important;}"
            ".widget-readout {color:white; !important; }"
            ".widget-output {color:white; !important; }"
            if theme_is_dark
            else ""
        )
        + "</style>"
    )
