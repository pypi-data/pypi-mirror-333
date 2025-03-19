# squall.py

from pathlib import Path
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center
from textual.widgets import Button, Footer, Header, Input
from textual.widgets import Label, TabbedContent, TabPane

from squall.database_structure_tree import DatabaseStructurePane
from squall.execute_sql import ExecuteSQLPane
from squall.screens import FileBrowser
from squall.table_viewer import TableViewerPane


class SQLiteClientApp(App):
    BINDINGS = [
        ("o", "open_database", "Open Database"),
        ("q", "quit", "Exit the program"),
    ]

    CSS_PATH = "squall.tcss"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = "Squall"

    def compose(self) -> ComposeResult:
        db_path = Input(id="db_path_input")
        db_path.border_title = "Database Path"
        yield Header()
        yield Center(
            Button("Open Database", id="open_db_btn", variant="primary"), id="center"
        )
        with TabbedContent("Database", id="tabbed_ui"):
            with TabPane("Database Structure"):
                yield Label("No data loaded")
            with TabPane("Table Viewer"):
                yield Label("No data loaded")
            with TabPane("Execute SQL"):
                yield Label("No data loaded")
        yield Footer()

    @on(Button.Pressed, "#open_db_btn")
    async def action_open_database(self) -> None:
        self.push_screen(FileBrowser(), self.update_ui)  # type: ignore

    async def update_ui(self, db_file_path: Path) -> None:
        if not Path(db_file_path).exists():
            self.notify("BAD PATH")
            return

        tabbed_content = self.query_one("#tabbed_ui", TabbedContent)
        await tabbed_content.clear_panes()

        await tabbed_content.add_pane(
            DatabaseStructurePane(
                db_file_path, title="Database Structure", id="db_structure"
            )
        )
        await tabbed_content.add_pane(
            TableViewerPane(db_file_path, title="Table Viewer")
        )
        await tabbed_content.add_pane(ExecuteSQLPane(db_file_path, title="Execute SQL"))
        tabbed_content.active = "db_structure"
        self.title = f"Squall - {db_file_path}"


def main() -> None:
    app = SQLiteClientApp()
    app.run()


if __name__ == "__main__":
    main()
