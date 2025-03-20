from typing import TYPE_CHECKING, cast

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMainWindow,
    QSplitter,
    QPushButton,
    QScrollArea,
    QInputDialog,
    QMessageBox,
    QApplication,
)
from PySide6.QtGui import QAction, QKeyEvent, QKeySequence
from PySide6.QtCore import Qt, QTimer, QLocale

from NeutroSpecUI.experiment_manager import ExperimentManager
from NeutroSpecUI.recent_files_menu import RecentFilesMenu

if TYPE_CHECKING:
    from NeutroSpecUI.app import NeutroApp


class NeutroSpecWindow(QMainWindow):
    """
    Provides a main application window with a menu bar and a text edit widget to display
    the content of a text or CSV file.
    """

    def __init__(self) -> None:
        """
        Initializes the main application window and sets up the user interface.
        """
        super().__init__()
        # ---------------------- Set up the main window ----------------------
        self.setWindowTitle("NeutronSpecUI")
        QLocale.setDefault(
            QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)
        )
        self.resize(800, 600)

        # Split the window into two parts
        splitter = QSplitter(self)
        self.setCentralWidget(splitter)

        self.left_widget = QWidget(splitter)
        self.left_layout = QVBoxLayout(self.left_widget)
        self.left_widget.setLayout(self.left_layout)
        self.left_widget.setMinimumWidth(220)
        splitter.addWidget(self.left_widget)

        self.right_widget = QWidget(splitter)
        self.right_layout = QVBoxLayout(self.right_widget)
        self.right_widget.setLayout(self.right_layout)
        splitter.addWidget(self.right_widget)

        # Create a scrollable container for the plot widgets
        self.right_scroll = QScrollArea(self.right_widget)
        self.right_scroll.setWidgetResizable(True)
        self.plot_container = QWidget(self.right_scroll)
        self.plot_layout = QVBoxLayout(self.plot_container)
        self.plot_container.setLayout(self.plot_layout)
        self.right_scroll.setWidget(self.plot_container)
        self.right_layout.addWidget(self.right_scroll)

        splitter.setSizes([220, 580])

        # ---------------------- Set up the experiment manager ----------------------
        self.experiment_manager = ExperimentManager(window=self, parent=self)

        submit_btn = QPushButton("Create Experiment")
        submit_btn.setObjectName("createExperiment")
        submit_btn.clicked.connect(self.create_experiment_dialog)
        self.addLeftWidget(submit_btn)

        self.addLeftWidget(self.experiment_manager)

        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(
            self.experiment_manager.update_all_plot_layouts
        )

        # ---------------------- Set up the menu bar ----------------------
        file_menu = self.menuBar().addMenu("File")
        file_menu.setObjectName("fileMenu")

        save_action = QAction("Save Setup", parent=file_menu)
        save_action.setObjectName("saveFileAction")
        save_action.triggered.connect(self.experiment_manager.save_dialog)
        file_menu.addAction(save_action)

        load_action = QAction("Open Setup", parent=file_menu)
        load_action.setObjectName("loadFileAction")
        load_action.triggered.connect(self.experiment_manager.load_dialog)
        file_menu.addAction(load_action)

        self.recent_files_menu = RecentFilesMenu(key="setups", parent=self)
        self.recent_files_menu.setTitle("Recent Files")
        self.recent_files_menu.load_file.connect(self.experiment_manager.load)
        file_menu.addMenu(self.recent_files_menu)

        settings_bar = self.menuBar().addMenu("Settings")
        sim_settings = QAction("Simulation", parent=settings_bar)
        sim_settings.setObjectName("simulationSettings")
        sim_settings.triggered.connect(self.open_settings_dialog)
        settings_bar.addAction(sim_settings)

    def addLeftWidget(self, widget: QWidget) -> None:
        widget.setParent(self.left_widget)
        self.left_layout.addWidget(widget)

    def addRightWidget(self, widget: QWidget) -> None:
        widget.setParent(self.right_widget)
        self.right_layout.addWidget(widget)

    def create_experiment_dialog(self):
        """
        Opens a dialog to get the name of the new experiment.
        """
        name, ok = QInputDialog.getText(self, "Create Experiment", "Experiment Name:")
        if ok and name:
            self.experiment_manager.create_empty_experiment(name=name)

    def addPlotWidget(self, widget: QWidget) -> None:
        widget.setParent(self.plot_container)
        self.plot_layout.addWidget(widget)

    def open_settings_dialog(self):
        app = cast("NeutroApp", QApplication.instance())
        has_changed = app.backend.open_settings_dialog()
        if has_changed:
            self.experiment_manager.update_all_plots()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Overrides the keyPressEvent to close the application when the Escape key is pressed,
        sets the application to Fullscreen on pressing f or f11, opens the save setup popup
        upon pressing ctrl + s and opens the load file popup upon pressing ctrl + o
        """
        if event.key() == Qt.Key.Key_Escape:
            reply = QMessageBox.question(
                self,
                "Close Application",
                "Do you really want to close the application?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.close()
        elif event.key() == Qt.Key.Key_F or event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif event.matches(QKeySequence.StandardKey.Save):
            self.experiment_manager.save_dialog()
        elif event.matches(QKeySequence.StandardKey.Open):
            self.experiment_manager.load_dialog()
        else:
            super().keyPressEvent(event)

    # TODO: move the resizing Event to the the plot container to account for splitter resizing
    def resizeEvent(self, event):
        """
        Overrides the resizeEvent to update the plot layout when the window is resized.
        """
        self.resize_timer.start(500)

        return super().resizeEvent(event)
