from textual.widget import Widget


class Header(Widget):
    DEFAULT_CSS = """
    Header {
        dock: top;
        width: 100%;
        background: $secondary;
        color: $text;
        height: 1;
        text-align: center;
    }
    """

    def __init__(self, title: str):
        self.title = title
        super().__init__()

    def render(self):
        return self.title
