from __future__ import annotations

import gradio as gr

from src.app_context import build_app_context
from src.ui.main import create_ui
from src.ui.styles import custom_css


def run() -> None:
    app_context = build_app_context()
    demo = create_ui(app_context)

    demo.launch(
        theme=gr.themes.Base(),
        css=custom_css,
    )


if __name__ == "__main__":
    run()