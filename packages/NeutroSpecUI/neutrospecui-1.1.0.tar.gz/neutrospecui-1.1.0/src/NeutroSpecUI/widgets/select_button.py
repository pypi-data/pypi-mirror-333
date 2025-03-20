from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMenu
from PySide6.QtCore import Signal


class SelectButton(QWidget):
    """A custom widget that displays a button with a dropdown menu to select an option.

    Attributes:
        clicked (Signal): Signal emits the selected option when the button is clicked.
    """

    clicked = Signal(str)

    def __init__(
        self,
        options: list[str],
        *,
        prefix: str = "",
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the SelectButton widget.

        Args:
            options (list[str]): A list of options to display in the dropdown menu.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.options = options
        self.prefix = prefix

        if len(options) == 0:
            options = ["No options available"]
        self.selected_option = options[0]

        self.right_button = QPushButton("", parent=self)
        self.right_button.setFixedWidth(30)
        self.update_menu()

        self.left_button = QPushButton(self.prefix + self.selected_option, parent=self)
        self.left_button.clicked.connect(self.trigger_option)

        # Create a horizontal layout to place the buttons side by side
        button_layout = QHBoxLayout()
        button_layout.setSpacing(0)  # Remove spacing between buttons
        button_layout.addWidget(self.left_button)
        button_layout.addWidget(self.right_button)

        # Create a container widget for the buttons
        button_container = QWidget()
        button_container.setLayout(button_layout)

        # Apply a border to the container to make it look like a single button
        button_container.setStyleSheet(
            """
            QWidget {
                border: 1px solid #000;
                border-radius: 5px;
            }
            QPushButton {
                border: none;
            }
            QPushButton:focus {
                outline: none;
            }
            """
        )

        layout = QVBoxLayout()
        layout.addWidget(button_container)
        self.setLayout(layout)

    def update_menu(self) -> None:
        menu = QMenu(self)

        if len(self.options) == 1:
            self.right_button.hide()
        else:
            self.right_button.show()

        for option in self.options:
            action = menu.addAction(option)
            action.triggered.connect(
                lambda checked, opt=option: self.select_option(opt)
            )

        self.right_button.setMenu(menu)

    def select_option(self, option: str) -> None:
        self.selected_option = option
        self.left_button.setText(self.prefix + self.selected_option)

    def trigger_option(self) -> None:
        self.clicked.emit(self.selected_option)
