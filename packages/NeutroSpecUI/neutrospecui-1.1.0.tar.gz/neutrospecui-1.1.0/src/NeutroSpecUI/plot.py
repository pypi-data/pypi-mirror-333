from typing import TYPE_CHECKING, cast

import matplotlib

matplotlib.use("QtAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QGroupBox,
    QButtonGroup,
    QPushButton,
    QApplication,
)
from PySide6.QtCore import Signal, QTimer

from NeutroSpecUI.data_models import ExperimentData

if TYPE_CHECKING:
    from NeutroSpecUI.app import NeutroApp


class CanvasWidget(FigureCanvasQTAgg):

    def __init__(self, parent: QWidget | None = None) -> None:
        app = cast("NeutroApp", QApplication.instance())
        self.fig, self.axes = app.backend.create_fig_axes()

        super().__init__(self.fig)
        if parent is not None:
            self.setParent(parent)

    def setParent(self, parent: QWidget | None) -> None:
        self._parent = parent

    def parent(self) -> QWidget | None:
        return self._parent

    def clear(self) -> None:
        for ax in self.axes:
            ax.clear()
        self.draw()


class PlotWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.setFixedHeight(350)

        self.canvas = CanvasWidget(self)
        self.toolbar = NavigationToolbar2QT(canvas=self.canvas, parent=self)
        self.toolbar.setIconSize(self.toolbar.iconSize() * 0.6)

        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.canvas)
        self.setLayout(self.main_layout)

    def display_loading(self, i: int) -> None:
        """Display a loading animation on the plot. The loading animation consists of a text that is updated every interval. The animation is based on the current step number.

        Args:
            i: Current step number of the loading animation.
        """
        self.canvas.clear()

        animation_step = i % 4
        loading_text = "Loading" + "." * animation_step

        for ax in self.canvas.axes:
            ax.text(0.5, 0.5, loading_text, ha="center", va="center", fontsize=18)
        self.canvas.fig.tight_layout()
        self.canvas.draw()


class PlotWidgetStacked(QStackedWidget):
    startLoadingAnimation = Signal()

    def __init__(self, exp_data: ExperimentData, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.exp_data = exp_data
        self.exp_data.updateData.connect(self.plot_sim)
        self.exp_data.updateData.connect(self.plot_fit)
        self.exp_data.updateData.connect(self.plot_compare)
        self.exp_data.updateSim.connect(self.plot_sim)
        self.exp_data.updateSim.connect(self.plot_compare)
        self.exp_data.updateFit.connect(self.plot_fit)
        self.exp_data.updateFit.connect(self.plot_compare)

        self.plots = {
            "simulate": PlotWidget(),
            "fit": PlotWidget(),
            "compare": PlotWidget(),
        }

        for plot_name, plot_widget in self.plots.items():
            self.addWidget(plot_widget)
            plot_widget.setObjectName(plot_name)

        self.loading_timer = LoadingAnimationTimer(parent=self)
        self.loading_timer.timeStep.connect(self.display_loading)

    def plot_sim(self) -> None:
        app = cast("NeutroApp", QApplication.instance())
        canvas = self.plots["simulate"].canvas

        canvas.clear()

        if self.exp_data.sim.data is not None:
            app.backend.plot_data(self.exp_data.sim.data, axes=canvas.axes)
        if self.exp_data.sim_result is not None:
            app.backend.plot_sim(self.exp_data.sim_result, axes=canvas.axes)

        canvas.fig.tight_layout()
        canvas.draw()

    def plot_fit(self) -> None:
        app = cast("NeutroApp", QApplication.instance())
        canvas = self.plots["fit"].canvas

        canvas.clear()

        if self.exp_data.sim.data is not None:
            app.backend.plot_data(self.exp_data.fit.data, axes=canvas.axes)
        if self.exp_data.fit_result is not None:
            app.backend.plot_fit(self.exp_data.fit_result, axes=canvas.axes)

        canvas.fig.tight_layout()
        canvas.draw()

    def plot_compare(self) -> None:
        app = cast("NeutroApp", QApplication.instance())
        canvas = self.plots["compare"].canvas

        canvas.clear()

        if self.exp_data.sim.data is not None:
            app.backend.plot_data(self.exp_data.fit.data, axes=canvas.axes)
        if self.exp_data.sim_result is not None:
            app.backend.plot_sim(self.exp_data.sim_result, axes=canvas.axes)
        if self.exp_data.fit_result is not None:
            app.backend.plot_fit(self.exp_data.fit_result, axes=canvas.axes)

        canvas.fig.tight_layout()
        canvas.draw()

    def display_loading(self, i: int) -> None:
        self.plots["fit"].display_loading(i)
        self.plots["compare"].display_loading(i)

    def update_plot_layout(self) -> None:
        for plot in self.plots.values():
            plot.canvas.fig.tight_layout()
            plot.canvas.draw()


from PySide6.QtCore import QTimer, Signal


class LoadingAnimationTimer(QTimer):
    """Timer for displaying a loading animation.

    The timer emits a `timeStep` signal every interval, which can be used to display a loading animation. The `timeStep` signal contains the number of the current step. Stopping the timer with `stopTimer` will reset the current step to 0.

    Attributes:
        timeStep: Signal emitted every interval with the current step number.
    """

    timeStep = Signal(int)

    def __init__(self, interval_msec: int = 300, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.current_step = 0
        self.setInterval(interval_msec)
        self.timeout.connect(self.emit_time_step)

    def emit_time_step(self):
        self.timeStep.emit(self.current_step)
        self.current_step += 1

    def stopTimer(self):
        self.stop()
        self.current_step = 0


class PlotButtons(QGroupBox):
    """
    Displays a group of three buttons for the three different plots.
    """

    idClicked = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(5, 0, 5, 5)
        self.setObjectName("plotViewOptions")

        self.btn_group = QButtonGroup(self.main_layout)
        self.btn_group.idClicked.connect(self.idClicked)

        self.simulate_btn = QPushButton("Simulate", self)
        self.simulate_btn.setObjectName("simulateViewBtn")
        self.simulate_btn.setCheckable(True)
        self.simulate_btn.setChecked(True)
        self.main_layout.addWidget(self.simulate_btn)
        self.btn_group.addButton(self.simulate_btn, 0)

        self.fit_btn = QPushButton("Fit", self)
        self.fit_btn.setObjectName("fitViewBtn")
        self.fit_btn.setCheckable(True)
        self.main_layout.addWidget(self.fit_btn)
        self.btn_group.addButton(self.fit_btn, 1)

        self.compare_btn = QPushButton("Compare", self)
        self.compare_btn.setObjectName("compareViewBtn")
        self.compare_btn.setCheckable(True)
        self.main_layout.addWidget(self.compare_btn)
        self.btn_group.addButton(self.compare_btn, 2)

        self.setLayout(self.main_layout)
