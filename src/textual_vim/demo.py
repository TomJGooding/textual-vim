from textual.app import App, ComposeResult

from textual_vim import VimEditor


class VimDemoApp(App):
    def compose(self) -> ComposeResult:
        yield VimEditor()


if __name__ == "__main__":
    app = VimDemoApp()
    app.run()
