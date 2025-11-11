import time
import typing
from core.base import Widget, draw_widget, add_widget_content, Config, UIState, BaseConfig


def draw(widget: Widget, ui_state: UIState, base_config: BaseConfig) -> None:
    content = [
        time.strftime(widget.config.weekday_format),
        time.strftime(widget.config.date_format),
        time.strftime(widget.config.time_format)
    ]
    draw_widget(widget, ui_state, base_config)
    add_widget_content(widget, content)


def build(stdscr: typing.Any, config: Config) -> Widget:
    return Widget(
        config.name, config.title, config, draw, config.interval, config.dimensions, stdscr
    )
