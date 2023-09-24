from pathlib import Path

from textual.app import App, ComposeResult

from textual_vim import VimEditor


class VimDemoApp(App):
    def compose(self) -> ComposeResult:
        yield VimEditor()

    def on_mount(self) -> None:
        vim_editor = self.query_one(VimEditor)
        tutor_path = Path(__file__).parent / "vimtutor.txt"
        with open(tutor_path, "r") as f:
            tutor_text = f.read()
        vim_editor.load_text(tutor_text)


if __name__ == "__main__":
    app = VimDemoApp()
    app.run()
