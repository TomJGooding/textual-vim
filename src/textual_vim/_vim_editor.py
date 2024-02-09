from __future__ import annotations

from dataclasses import dataclass

from textual import actions, events, on
from textual._callback import invoke
from textual.app import ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Input, Static, TextArea
from textual.widgets.text_area import Location
from typing_extensions import Literal, override


@dataclass
class Command:
    key: str
    action: str


_COMMANDS = [
    # Left-right motions
    Command("h", "left"),
    Command("l", "right"),
    Command("0", "line_start(False)"),  # first_nonwhite=False
    Command("^", "line_start(True)"),  # first_nonwhite=True
    Command("$", "line_end"),
    # Up-down motions
    Command("k", "up"),
    Command("j", "down"),
    Command("G", "last_line"),
    Command("g", "first_line"),
    # TODO: Text object motions
    # ...
    # Inserting text
    Command("a", "edit('a')"),
    Command("A", "edit('A')"),
    Command("i", "edit('i')"),
    Command("I", "edit('I')"),
    Command("o", "open_line('o')"),
    Command("O", "open_line('O')"),
    # Deleting text
    Command("x", "delete('x')"),
    Command("X", "delete('X')"),
    Command("D", "delete('D')"),
    # TODO: copying and moving text
    # ...
    # Changing text
    Command("C", "delete('C')"),
]


class ModeDisplay(Static):
    DEFAULT_CSS = """
    ModeDisplay {
        width: 1fr;
        text-style: bold;
    }
    """


class CommandRegister(Input, inherit_bindings=False):
    DEFAULT_CSS = """
    CommandRegister {
        height: 1;
        width: 10;
        border: none;
        padding: 0;
    }

    CommandRegister:focus {
        border: none;
    }

    CommandRegister>.input--cursor {
        color: $boost;
    }
    """

    def on_mount(self) -> None:
        self.cursor_blink = False


class StatusLine(Widget):
    DEFAULT_CSS = """
    StatusLine {
        height: 1;
        layout: horizontal;
        background: #272822;
    }
    """

    def compose(self) -> ComposeResult:
        yield ModeDisplay()
        yield CommandRegister()


class VimTextArea(TextArea, inherit_bindings=False):
    DEFAULT_CSS = """
    VimTextArea {
        scrollbar-size: 0 0;
        border: none;
        padding: 0;
    }

    VimTextArea:focus {
        border: none;
        padding: 0;
    }
    """

    BINDINGS = [
        Binding("backspace", "delete_left", "delete left", show=False),
        Binding("escape", "screen.focus_next", "Shift Focus", show=False),
        Binding("up", "cursor_up", "cursor up", show=False),
        Binding("down", "cursor_down", "cursor down", show=False),
        Binding("left", "cursor_left", "cursor left", show=False),
        Binding("right", "cursor_right", "cursor right", show=False),
        # Binding("shift+left", "cursor_word_left", "cursor word left", show=False),
        # Binding("shift+right", "cursor_word_right", "cursor word right", show=False),
        Binding("home", "cursor_line_start", "cursor line start", show=False),
        Binding("end", "cursor_line_end", "cursor line end", show=False),
        Binding("pageup", "cursor_page_up", "cursor page up", show=False),
        Binding("pagedown", "cursor_page_down", "cursor page down", show=False),
    ]

    class Blurred(Message):
        def __init__(self, vim_text_area: VimTextArea) -> None:
            super().__init__()
            self.vim_text_area = vim_text_area

        @property
        def control(self) -> VimTextArea:
            return self.vim_text_area

    class Focused(Message):
        def __init__(self, vim_text_area: VimTextArea) -> None:
            super().__init__()
            self.vim_text_area = vim_text_area

        @property
        def control(self) -> VimTextArea:
            return self.vim_text_area

    def __init__(
        self,
        text: str = "",
        *,
        language: str | None = None,
        theme: str | None = "monokai",
        soft_wrap: bool = False,
        tab_behaviour: Literal["focus", "indent"] = "indent",
        show_line_numbers: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            text,
            language=language,
            theme=theme,
            soft_wrap=soft_wrap,
            tab_behaviour=tab_behaviour,
            show_line_numbers=show_line_numbers,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    @override
    def watch_has_focus(self, value: bool) -> None:
        super().watch_has_focus(value)
        self._cursor_visible = True

    @override
    def action_cursor_left(self, select: bool = False) -> None:
        new_cursor_location = self.get_cursor_left_no_wrap_location()
        self.move_cursor(new_cursor_location, select=select)

    @override
    def action_cursor_right(self, select: bool = False) -> None:
        new_cursor_location = self.get_cursor_right_no_wrap_location()
        self.move_cursor(new_cursor_location, select=select)

    def get_cursor_left_no_wrap_location(self) -> Location:
        if self.cursor_at_start_of_text:
            return 0, 0
        cursor_row, cursor_column = self.selection.end
        target_row = cursor_row
        target_column = cursor_column - 1 if cursor_column != 0 else cursor_column
        return target_row, target_column

    def get_cursor_right_no_wrap_location(self) -> Location:
        if self.cursor_at_end_of_text:
            return self.selection.end
        cursor_row, cursor_column = self.selection.end
        target_row = cursor_row
        target_column = (
            cursor_column + 1 if not self.cursor_at_end_of_line else cursor_column
        )
        return target_row, target_column

    @override
    def get_cursor_up_location(self) -> Location:
        cursor_row, cursor_column = self.selection.end
        if self.cursor_at_first_line:
            return cursor_row, cursor_column

        # TODO: TextArea no longer has _last_intentional_cell_widgth after v0.48!
        return super().get_cursor_up_location()
        # target_row = max(0, cursor_row - 1)
        # # Attempt to snap last intentional cell length
        # target_column = self.cell_width_to_column_index(
        #     self._last_intentional_cell_width, target_row
        # )
        # target_column = clamp(target_column, 0, len(self.document[target_row]))
        # return target_row, target_column

    @override
    def _on_blur(self, _: events.Blur) -> None:
        self._pause_blink(visible=True)
        self.action_cursor_left()
        self.post_message(self.Blurred(self))

    @override
    def _on_focus(self, _: events.Focus) -> None:
        self._restart_blink()
        self.post_message(self.Focused(self))


class VimEditor(Widget):
    def compose(self) -> ComposeResult:
        yield VimTextArea()
        yield StatusLine()

    def on_mount(self) -> None:
        self.query_one(CommandRegister).focus()

    def start_insert_mode(self) -> None:
        self.query_one(ModeDisplay).update("-- INSERT --")
        self.query_one(TextArea).focus()

    def end_insert_mode(self) -> None:
        self.query_one(ModeDisplay).update()
        self.query_one(CommandRegister).focus()

    def load_text(self, text: str) -> None:
        self.query_one(TextArea).load_text(text)

    @on(VimTextArea.Blurred)
    def on_vim_text_area_blurred(self) -> None:
        self.end_insert_mode()

    @on(VimTextArea.Focused)
    def on_vim_text_area_focused(self) -> None:
        self.start_insert_mode()

    @on(CommandRegister.Changed)
    async def on_command_register_changed(
        self,
        event: CommandRegister.Changed,
    ) -> None:
        if not event.value:
            return
        last_key = event.value[-1]
        command = self._find_command(last_key)
        if command is not None:
            action_name, params = actions.parse(command.action)
            method = getattr(self, f"_{action_name}", None)
            if method:
                await invoke(method, *params)
                self.query_one(CommandRegister).clear()

    def _find_command(self, key: str) -> Command | None:
        for command in _COMMANDS:
            if command.key == key:
                return command
        return None

    # Left-right motions

    def _left(self) -> None:
        self.query_one(TextArea).action_cursor_left()

    def _right(self) -> None:
        self.query_one(TextArea).action_cursor_right()

    def _line_start(self, first_nonwhite: bool) -> None:
        text_area = self.query_one(TextArea)
        target = text_area.get_cursor_line_start_location(first_nonwhite)
        text_area.move_cursor(target)

    def _line_end(self) -> None:
        self.query_one(TextArea).action_cursor_line_end()

    # Up-down motions

    def _up(self) -> None:
        self.query_one(TextArea).action_cursor_up()

    def _down(self) -> None:
        self.query_one(TextArea).action_cursor_down()

    def _first_line(self) -> None:
        text_area = self.query_one(TextArea)
        _, cursor_column = text_area.cursor_location
        text_area.move_cursor((0, cursor_column))

    def _last_line(self) -> None:
        text_area = self.query_one(TextArea)
        last_line = text_area.document.line_count - 1
        _, cursor_column = text_area.cursor_location
        text_area.move_cursor((last_line, cursor_column))

    # Inserting text

    def _edit(self, key: str) -> None:
        text_area = self.query_one(TextArea)
        if key == "a":
            text_area.action_cursor_right()
        elif key == "A":
            text_area.action_cursor_line_end()
        elif key == "i":
            pass
        elif key == "I":
            text_area.action_cursor_line_start()
        self.start_insert_mode()

    def _open_line(self, key: str) -> None:
        text_area = self.query_one(TextArea)
        cursor_row, _ = text_area.cursor_location
        new_line = text_area.document.newline
        if key == "o":
            new_line = text_area.document.newline
            text_area.insert(new_line, (cursor_row + 1, 0))
        elif key == "O":
            text_area.insert(new_line, (cursor_row, 0))
            text_area.action_cursor_up()
        self.start_insert_mode()

    # Deleting text

    def _delete(self, key: str) -> None:
        text_area = self.query_one(TextArea)
        if key == "x":
            if not text_area.cursor_at_end_of_line:
                text_area.action_delete_right()
                if text_area.cursor_at_end_of_line:
                    text_area.action_cursor_left()
        elif key == "X":
            if not text_area.cursor_at_start_of_line:
                text_area.action_delete_left()
        elif key == "D":
            text_area.action_delete_to_end_of_line()
            text_area.action_cursor_left()
        elif key == "C":
            text_area.action_delete_to_end_of_line()
            self.start_insert_mode()
