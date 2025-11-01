import time
import typing
from core.base import Widget, draw_widget, add_widget_content, Config


def draw(widget: Widget) -> None:
    content = [
        time.strftime(widget.config.weekday_format),
        time.strftime(widget.config.date_format),
        time.strftime(widget.config.time_format)
    ]
    draw_widget(widget)
    add_widget_content(widget, content)


def build(stdscr: typing.Any, config: Config) -> Widget:
    return Widget(
        config.name, config.title, config, draw, config.interval, config.dimensions, stdscr
    )
