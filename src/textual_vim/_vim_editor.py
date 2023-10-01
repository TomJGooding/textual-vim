from __future__ import annotations

from textual import events, on
from textual.app import ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Input, Static, TextArea
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


class VimTextArea(TextArea):
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
        # Insert or append text
        if event.value[-1] == "i":
            self.start_insert_mode()
            command_complete = True
        elif event.value[-1] == "a":
            text_area.action_cursor_right()
            self.start_insert_mode()
            command_complete = True
        # Moving the cursor
        elif event.value[-1] == "h":
            text_area.action_cursor_left()
            command_complete = True
        elif event.value[-1] == "j":
            text_area.action_cursor_down()
            command_complete = True
        elif event.value[-1] == "k":
            text_area.action_cursor_up()
            command_complete = True
        elif event.value[-1] == "l":
            text_area.action_cursor_right()
            command_complete = True
        # Deletion
        elif event.value[-1] == "x":
            text_area.action_delete_right()
            text_area.action_cursor_left()
            command_complete = True
        # Basic motions
        elif event.value[-1] == "w":
            text_area.action_cursor_word_right()
            text_area.action_cursor_word_right()
            text_area.action_cursor_word_left()
            command_complete = True
        elif event.value[-1] == "e":
            text_area.action_cursor_word_right()
            text_area.action_cursor_left()
            command_complete = True
        elif event.value[-1] == "$":
            text_area.action_cursor_line_end()
            text_area.action_cursor_left()
            command_complete = True

        if command_complete:
            event.input.value = ""

    @on(VimTextArea.Blurred)
    def on_vim_text_area_blurred(self) -> None:
        self.end_insert_mode()

    @on(VimTextArea.Focused)
    def on_vim_text_area_focused(self) -> None:
        self.start_insert_mode()
