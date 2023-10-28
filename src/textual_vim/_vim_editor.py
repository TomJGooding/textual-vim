from __future__ import annotations

from textual import events, on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.geometry import clamp
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Input, Static, TextArea
from textual.widgets.text_area import Location
from typing_extensions import override


class CommandRegister(Input):
    DEFAULT_CSS = """
    CommandRegister {
        height: 0;
        width: 0;
        min-height: 0;
        min-width: 0;
        border: none;
        background: red;
    }

    CommandRegister:focus {
        border: none;
    }
    """


class StatusLine(Static):
    DEFAULT_CSS = """
    StatusLine {
        text-style: bold;
        background: #272822;
    }
    """


class VimTextArea(TextArea, inherit_bindings=False):
    DEFAULT_CSS = """
    VimTextArea {
        scrollbar-size: 0 0;
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
        target_row = max(0, cursor_row - 1)
        # Attempt to snap last intentional cell length
        target_column = self.cell_width_to_column_index(
            self._last_intentional_cell_width, target_row
        )
        target_column = clamp(target_column, 0, len(self.document[target_row]))
        return target_row, target_column

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
        yield CommandRegister()
        yield StatusLine()

    def on_mount(self) -> None:
        self.query_one(CommandRegister).focus()

    def start_insert_mode(self) -> None:
        self.query_one(StatusLine).update("-- INSERT --")
        self.query_one(VimTextArea).focus()

    def end_insert_mode(self) -> None:
        self.query_one(StatusLine).update()
        self.query_one(CommandRegister).focus()

    def load_text(self, text: str) -> None:
        text_area = self.query_one(VimTextArea)
        text_area.load_text(text)

    @on(CommandRegister.Changed)
    def on_command_register_changed(self, event: CommandRegister.Changed) -> None:
        text_area = self.query_one(VimTextArea)
        command_complete = False
        if not event.value:
            return

        # Left-right motions
        if event.value[-1] == "h":
            text_area.action_cursor_left()
            command_complete = True
        elif event.value[-1] == "l":
            text_area.action_cursor_right()
            command_complete = True
        elif event.value[-1] == "0":
            cursor_row, _ = text_area.cursor_location
            text_area.move_cursor((cursor_row, 0))
            command_complete = True
        elif event.value[-1] == "^":
            text_area.action_cursor_line_start()
            command_complete = True
        elif event.value[-1] == "$":
            text_area.action_cursor_line_end()
            text_area.action_cursor_left()
            command_complete = True

        # Up-down motions
        elif event.value[-1] == "k":
            text_area.action_cursor_up()
            command_complete = True
        elif event.value[-1] == "j":
            text_area.action_cursor_down()
            command_complete = True
        elif event.value[-1] == "G":
            last_line = text_area.document.line_count - 1
            _, cursor_column = text_area.cursor_location
            text_area.move_cursor((last_line, cursor_column))
            command_complete = True
        elif event.value[-2:] == "gg":
            _, cursor_column = text_area.cursor_location
            text_area.move_cursor((0, cursor_column))
            command_complete = True

        # TODO: Text object motions

        # Inserting text
        elif event.value[-1] == "a":
            text_area.action_cursor_right()
            self.start_insert_mode()
            command_complete = True
        elif event.value[-1] == "A":
            text_area.action_cursor_line_end()
            self.start_insert_mode()
            command_complete = True
        elif event.value[-1] == "i":
            self.start_insert_mode()
            command_complete = True
        elif event.value[-1] == "I":
            text_area.action_cursor_line_start()
            self.start_insert_mode()
            command_complete = True

        # Deleting text
        elif event.value[-1] == "x":
            text_area.action_delete_right()
            text_area.action_cursor_left()
            command_complete = True

        # TODO: Copying and moving text

        # TODO: Changing text

        if command_complete:
            event.input.value = ""

    @on(VimTextArea.Blurred)
    def on_vim_text_area_blurred(self) -> None:
        self.end_insert_mode()

    @on(VimTextArea.Focused)
    def on_vim_text_area_focused(self) -> None:
        self.start_insert_mode()
