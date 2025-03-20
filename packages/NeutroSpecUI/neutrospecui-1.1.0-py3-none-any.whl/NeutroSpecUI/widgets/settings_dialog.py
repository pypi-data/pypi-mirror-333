from ast import literal_eval

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QWidget,
    QDialogButtonBox,
    QErrorMessage,
)


class SettingsDialog(QDialog):
    """A dialog to edit the settings for the simulation.

    This dialog allows the user to edit the settings for the simulation. The settings are stored in a dictionary and can be edited using this dialog. The dialog will return the new settings when the user clicks the `OK` button.
    """

    def __init__(self, settings: dict, parent=None):
        """Initializes the dialog with the given settings.

        Args:
            settings (dict): The settings dictionary to edit.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.settings: dict = {}
        self.setWindowTitle("Edit Settings")

        layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.fields: dict[str, QLineEdit] = {}
        for key, value in settings.items():
            label = QLabel(key)
            field = QLineEdit(str(value))
            self.fields[key] = field
            self.form_layout.addRow(label, field)

        layout.addLayout(self.form_layout)

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

        self.setLayout(layout)

    def accept(self):
        """Accepts the dialog and returns the new settings."""
        for key, field in self.fields.items():
            try:
                self.settings[key] = literal_eval(field.text())
            except ValueError as e:
                error_dialog = QErrorMessage(parent=self)
                error_dialog.showMessage(
                    f'Error parsing value for "{key}": "{field.text()}"'
                )
                return

        super().accept()

    @staticmethod
    def get_settings(settings: dict, parent: QWidget | None = None) -> dict:
        """Opens the dialog and returns the new settings.

        This static method opens the dialog with the given settings and returns the new settings after the user closes the dialog.

        Args:
            settings (dict): The settings dictionary to edit.
            parent (QWidget, optional): The parent widget. Defaults to None.

        Returns:
            dict: The new settings after the user closes the dialog.
        """
        dialog = SettingsDialog(settings, parent)
        result = dialog.exec_()
        if result == QDialog.DialogCode.Accepted:
            return dialog.settings
        return settings
