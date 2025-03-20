import math

from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QSpinBox,
)

from NeutroSpecUI.data_models import Parameter


class ParameterDetailView(QDialog):
    """A dialog for displaying and editing a single parameter

    This dialog displays a parameter's name, value, locked status, unit, and factor.
    It allows the user to edit these values and save the changes.

    Attributes:
        valueUpdate (Signal): Signal emitted when the parameter value is updated (emitted on save)
    """

    valueUpdate = Signal()

    def __init__(self, parameter: Parameter, parent=None):
        super().__init__(parent)
        self.parameter = parameter
        self.setWindowTitle("Parameter Detail View")
        self.setModal(True)

        layout = QVBoxLayout()

        # Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:", self)
        self.name_input = QLineEdit(self)
        self.name_input.setText(self.parameter.name)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Value
        value_layout = QHBoxLayout()
        value_label = QLabel("Value:", self)
        self.value_input = QLineEdit(self)
        self.value_input.setValidator(QDoubleValidator(self))
        self.value_input.setText(str(self.parameter.value))
        value_layout.addWidget(value_label)
        value_layout.addWidget(self.value_input)
        layout.addLayout(value_layout)

        # Locked
        locked_layout = QHBoxLayout()
        locked_label = QLabel("Locked:", self)
        self.locked_checkbox = QCheckBox(self)
        self.locked_checkbox.setChecked(self.parameter.locked)
        locked_label.setToolTip("Locked parameters will not be optimized")
        self.locked_checkbox.setToolTip("Locked parameters will not be optimized")
        locked_layout.addWidget(locked_label)
        locked_layout.addWidget(self.locked_checkbox)
        layout.addLayout(locked_layout)

        # Unit
        unit_layout = QHBoxLayout()
        unit_label = QLabel("Unit:", self)
        self.unit_input = QLineEdit(self)
        self.unit_input.setText(self.parameter.unit)
        unit_layout.addWidget(unit_label)
        unit_layout.addWidget(self.unit_input)
        layout.addLayout(unit_layout)

        # Factor
        factor_layout = QHBoxLayout()
        factor_label = QLabel("Factor: \u00d710^", self)
        self.factor_input = QSpinBox(self)
        self.factor_input.setRange(-100, 100)
        self.factor_input.setValue(int(math.log10(self.parameter.factor)))
        self.factor_input.setToolTip("Power of 10 to multiply the value by")
        factor_layout.addWidget(factor_label)
        factor_layout.addWidget(self.factor_input)
        layout.addLayout(factor_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save)
        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save(self):
        """Save the parameter values and emit the valueUpdate signal"""
        self.parameter.name = self.name_input.text()
        self.parameter.value = float(self.value_input.text())
        self.parameter.locked = self.locked_checkbox.isChecked()
        self.parameter.unit = self.unit_input.text()
        self.parameter.factor = 10 ** self.factor_input.value()

        self.valueUpdate.emit()
        self.accept()
