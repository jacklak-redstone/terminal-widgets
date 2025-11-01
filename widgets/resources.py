import random
import typing
from core.base import Widget, draw_widget, add_widget_content, Config


def update(_widget: Widget) -> list[str]:
    """
    used_mem: int | float = round(memory.used / (1024 ** 2), 2)
    total_mem: int | float = round(memory.total / (1024 ** 2), 2)
    used_disk: int | float = round(disk_usage.used / (1024 ** 3), 2)
    total_disk: int | float = round(disk_usage.total / (1024 ** 3), 2)
    """

    return [f'{random.randint(0, 10**10):010}' for _ in range(8)]


def draw(widget: Widget, content: list[str]) -> None:
    draw_widget(widget)
    add_widget_content(widget, content)


def build(stdscr: typing.Any, config: Config) -> Widget:
    return Widget(
        config.name, config.title, config, draw, config.interval, config.dimensions, stdscr, update
    )
