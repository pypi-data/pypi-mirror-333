from rich import markup
from textual import work
from textual.widgets import Static
from tooi.utils import images


class HalfblockImage(Static):
    def __init__(
        self,
        path_or_url: str,
        width: int,
        height: int,
        *,
        id: str | None = None,
        classes: str | None = None,
        blurhash: str | None = None,
        aspect_ratio: float | None = None,
    ):
        self.path_or_url = path_or_url
        self.width = width
        self.height = height

        # TODO: dynamic size based on viewport?
        placeholder = images.render_placeholder(width, height, blurhash, aspect_ratio)
        super().__init__(placeholder, id=id, classes=classes)

    async def on_mount(self):
        self.call_after_refresh(self.render_image)

    @work
    async def render_image(self):
        try:
            if self.path_or_url.lower().startswith("http"):
                import asyncio
                await asyncio.sleep(1)
                rendered = await images.render_remote(self.path_or_url, self.width, self.height)
            else:
                rendered = await images.render_local(self.path_or_url, self.width, self.height)

            self.update(rendered)
        except Exception as ex:
            self.show_error(f"Failed loading image:\n{ex}")

    def show_error(self, error: str):
        self.update(f"[red]{markup.escape(error)}[/]")
