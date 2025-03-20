from collections.abc import Callable
from typing import cast

from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QWidget,
    QPushButton,
    QCheckBox,
    QSizePolicy,
    QToolButton,
)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Signal

from NeutroSpecUI.data_models import Material, Parameter
from NeutroSpecUI.widgets.parameter_details import ParameterDetailView


class MaterialWidget(QFrame):
    """A widget for displaying and editing a single material

    This widget displays a material's name and parameters.
    It also provides a button to remove the material from the list.

    Attributes:
        valueUpdate (Signal): Signal emitted when the material value is updated
    """

    valueUpdate = Signal()

    def __init__(
        self,
        material: Material,
        closed: bool = False,
        parent: QWidget | None = None,
        remove: Callable[["MaterialWidget"], None] = lambda x: None,
    ) -> None:
        super().__init__(parent)
        self.material = material
        self.closed = closed

        self.setFrameStyle(QFrame.Shape.Box)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.my_layout = QVBoxLayout(self)
        self.my_layout.setSpacing(0)
        self.my_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.my_layout)

        # Create a horizontal layout for the header
        self.header_layout = QHBoxLayout()
        self.my_layout.insertLayout(0, self.header_layout)

        # Add the AttributeInputField for the material name
        name = AttributeInputField(self, "name", parent=self)
        name.valueUpdate.connect(self.valueUpdate)
        self.header_layout.addWidget(name)

        # Add a spacer to push the delete button to the right
        self.header_layout.addStretch()

        # Add the toggle button
        self.toggle_button = QPushButton("▼", self)
        self.toggle_button.setFixedSize(20, 20)
        self.toggle_button.setStyleSheet("QPushButton { border: none; }")
        self.toggle_button.setToolTip("Toggle Material Details")
        self.toggle_button.clicked.connect(self.toggle)
        self.header_layout.addWidget(self.toggle_button)

        # Add remove button
        self.remove_button = QPushButton("x", self)
        self.remove_button.setObjectName("deleteMaterialBtn")
        self.remove_button.setToolTip("Delete Material")
        self.remove_button.setFixedSize(20, 20)
        self.remove_button.setStyleSheet(
            "QPushButton { border: none; padding-top: -5px; }"
        )
        self.remove_button.clicked.connect(lambda: remove(self))
        self.remove_button.clicked.connect(self.valueUpdate)
        self.header_layout.addWidget(self.remove_button)

        # Add material name and parameters
        for param in self.material.params:
            param_input = ParameterInputField(param, parent=self)
            param_input.valueUpdate.connect(self.valueUpdate)
            self.my_layout.addWidget(param_input)

        # Set initial visibility based on the closed state
        self.set_material_details_visibility(not self.closed)

    def toggle(self) -> None:
        self.closed = not self.closed
        self.set_material_details_visibility(not self.closed)
        self.toggle_button.setText("▲" if self.closed else "▼")

    def set_material_details_visibility(self, visible: bool) -> None:
        for i in range(1, self.my_layout.count()):
            widget = self.my_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(visible)

    def update_fitting_fields(self, fitted_material: Material) -> None:
        for i, param in enumerate(fitted_material.params):
            param_input = cast(
                "ParameterInputField", self.my_layout.itemAt(i + 1).widget()
            )
            param_input.update_fitted_field(param)


class AttributeInputField(QWidget):
    valueUpdate = Signal()

    def __init__(
        self, mat_widget: MaterialWidget, attr_name: str, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)

        layout = QHBoxLayout(self)
        self.setLayout(layout)

        input_field = QLineEdit(self)
        input_field.setFixedHeight(20)
        input_field.setText(getattr(mat_widget.material, attr_name))
        input_field.setObjectName(f"{attr_name}Input")
        input_field.editingFinished.connect(self.valueUpdate)

        layout.addWidget(input_field)

        input_field.textChanged.connect(
            lambda text: setattr(mat_widget.material, attr_name, str(text))
        )


class ParameterInputField(QFrame):
    """A widget for displaying and editing a single parameter

    This widget displays a parameter's name, value, and locked status.
    It also provides a button to open a dialog for editing the parameter's details.

    Attributes:
        valueUpdate (Signal): Signal emitted when the parameter value is updated
    """

    valueUpdate = Signal()

    def __init__(self, param: Parameter, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._param = param

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(5, 0, 5, 0)

        # Create widgets
        self.input_field = QLineEdit(self)
        validator = QDoubleValidator(self.input_field)
        self.input_field.setValidator(validator)
        self.input_field.setText(str(param.value))
        self.input_field.setFixedHeight(20)
        self.input_field.setObjectName(f"{param.name}Input")
        # TODO: signal is currently emitted on the first focus out event after creation
        # it would be good to fix that behavior an only emit after truly editing the value

        self.fitted_btn = QPushButton(self)
        self.fitted_btn.setFixedHeight(20)
        self.fitted_btn.setText("-")
        self.fitted_btn.setObjectName(f"{param.name}Fitted")

        self.label = QLabel("Parameter", self)
        self.label.setFixedHeight(20)

        self.checkbox = QCheckBox("locked", self)
        self.checkbox.setToolTip("Locked parameters will not be optimized")
        self.checkbox.setFixedHeight(20)
        self.checkbox.setObjectName(f"{param.name}SetLocked")

        details_btn = QToolButton(self)
        details_btn.setText("⚙️")
        details_btn.setFixedHeight(20)
        details_btn.clicked.connect(lambda: self.open_detail_view(self._param))

        # Set initial values
        self.update_param()

        # Add widgets to layout
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.checkbox, 0, 1)
        layout.addWidget(details_btn, 0, 2)
        layout.addWidget(self.input_field, 1, 0)
        layout.addWidget(self.fitted_btn, 1, 1, 1, 2)

        # Connect signals
        self.fitted_btn.clicked.connect(self.update_param_value_with_fit)
        validator = QDoubleValidator(self.input_field)
        self.input_field.setValidator(validator)
        self.input_field.textChanged.connect(
            lambda text: setattr(param, "value", validator.locale().toDouble(text)[0])
        )
        self.checkbox.stateChanged.connect(
            lambda state: setattr(param, "locked", state == 2)
        )
        self.input_field.editingFinished.connect(self.valueUpdate)

    def update_param(self) -> None:
        """Update the displayed parameter values"""
        label_str = (
            f"{self._param.name} ({self._param.unit})"
            if self._param.unit
            else self._param.name
        )
        self.label.setText(label_str)

        self.checkbox.setChecked(self._param.locked)
        self.input_field.setText(str(self._param.value))

    def open_detail_view(self, param: Parameter) -> None:
        """Open a dialog to edit the parameter details"""
        dialog = ParameterDetailView(param, self)
        dialog.valueUpdate.connect(self.update_param)
        dialog.valueUpdate.connect(self.valueUpdate)
        dialog.exec()

    def update_fitted_field(self, param: Parameter) -> None:
        if not param.locked:
            self.fitted_btn.setText(str(param.value))

    def update_param_value_with_fit(self) -> None:
        if self.fitted_btn.text() != "-":
            self.input_field.setText(self.fitted_btn.text())
            self.valueUpdate.emit()
