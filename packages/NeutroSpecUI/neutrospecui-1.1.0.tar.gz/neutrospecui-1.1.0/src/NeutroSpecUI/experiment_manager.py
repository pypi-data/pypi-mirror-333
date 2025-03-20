import json
from dataclasses import asdict, is_dataclass
from typing import TYPE_CHECKING, cast

from PySide6.QtWidgets import (
    QTabWidget,
    QFileDialog,
    QDialog,
    QHBoxLayout,
    QLineEdit,
    QApplication,
)
from NeutroSpecUI.experimental_setup import ExperimentalSetup
from NeutroSpecUI.plot import PlotButtons

if TYPE_CHECKING:
    from NeutroSpecUI.main_window import NeutroSpecWindow
    from NeutroSpecUI import NeutroApp


class ExperimentManager(QTabWidget):
    def __init__(self, window: "NeutroSpecWindow", parent=None) -> None:
        super().__init__(parent)
        self.main_window = window
        self.plot_btn_switch = PlotButtons(self.main_window)
        self.main_window.addRightWidget(self.plot_btn_switch)
        self.tabBarDoubleClicked.connect(self.edit_tab)

        self.tabBar().setMovable(True)

    def edit_tab(self, index: int) -> None:
        change_name_dialog = ChangeExperimentName(self, self.tabText(index), self)
        change_name_dialog.exec()

    def add_experiment(self, exp: ExperimentalSetup) -> None:
        self.addTab(exp, exp.name)
        self.plot_btn_switch.idClicked.connect(exp.plot.setCurrentIndex)

    def create_empty_experiment(self, name: str) -> ExperimentalSetup:
        exp = ExperimentalSetup(window=self.main_window, name=name, parent=self)
        self.add_experiment(exp)
        return exp

    def get_experiments(self) -> list[ExperimentalSetup]:
        return [cast(ExperimentalSetup, self.widget(i)) for i in range(self.count())]

    def clear(self) -> None:
        for exp in self.get_experiments():
            self.removeTab(self.indexOf(exp))
            exp.deleteLater()

    def update_all_plots(self) -> None:
        for exp in self.get_experiments():
            exp.materialUpdate.emit()

    def update_all_plot_layouts(self) -> None:
        for exp in self.get_experiments():
            exp.plot.update_plot_layout()

    def save_dialog(self) -> None:
        file_name, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save File",
            dir="",  # TODO: remember last directory
            filter="JSON Files (*.json)",
        )

        if not file_name:
            return

        self.save(file_name)

    def save(self, file_name: str) -> None:
        with open(file_name, "w") as file:
            json.dump(self.to_dict(), file, indent=4, cls=EnhancedJSONEncoder)
            self.main_window.recent_files_menu.add_file_to_recent(file_name)
            print("File created in path:", file_name)

    def load_dialog(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Load File",
            dir="",  # TODO: remember last directory
            filter="JSON Files (*.json)",
        )

        if not file_name:
            return

        self.load(file_name)

    def load(self, file_name: str) -> None:
        with open(file_name, "r") as file:
            data = json.load(file)
            self.main_window.recent_files_menu.add_file_to_recent(file_name)
            self.from_dict(data)

    def to_dict(self) -> dict:
        app = cast("NeutroApp", QApplication.instance())
        settings = app.backend.get_settings()
        return {
            "experimental_setups": [exp.to_dict() for exp in self.get_experiments()],
            "simulation_settings": settings,
        }

    def from_dict(self, data: dict) -> None:
        self.clear()
        for exp_data in data["experimental_setups"]:
            exp = self.create_empty_experiment(exp_data["name"])
            exp.from_dict(exp_data)

        if "simulation_settings" in data:
            app = cast("NeutroApp", QApplication.instance())
            app.backend.set_settings(data["simulation_settings"])


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)  # type: ignore
        return super().default(o)


class ChangeExperimentName(QDialog):
    def __init__(self, parent=None, current_text="", current_tab=QTabWidget) -> None:
        super().__init__(parent)
        self.current_text = current_text
        self.current_tab = current_tab
        self.make_dialog(current_text)

    def make_dialog(self, current_text):
        self.resize(300, 100)
        self.setWindowTitle("Change Experiment Name")
        h_layout = QHBoxLayout()
        self.Input = QLineEdit(current_text, self)
        h_layout.addWidget(self.Input)
        self.Input.editingFinished.connect(self.change_tab_name)
        self.Input.setFocus()
        self.setLayout(h_layout)

    def change_tab_name(self) -> None:
        new_text = self.Input.text()
        self.current_tab.setTabText(self.current_tab.currentIndex(), new_text)
        exp_setup = cast("ExperimentalSetup", self.current_tab.currentWidget())
        exp_setup.name = new_text
        exp_setup.setObjectName(new_text)
        self.accept()
