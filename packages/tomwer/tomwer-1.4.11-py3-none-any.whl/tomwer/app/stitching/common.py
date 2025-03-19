"""Common module for y and z stitcher"""

from __future__ import annotations

import argparse
import logging
import signal
import sys
import functools

from tqdm import tqdm

import silx
from silx.gui import qt

from nabu.pipeline.config import generate_nabu_configfile
from nabu.stitching.config import get_default_stitching_config, SECTIONS_COMMENTS
import os
from nabu.stitching.config import StitchingType

from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.core.settings import SlurmSettingsMode
from tomwer.core.utils.resource import increase_max_number_file
from tomwer.gui import icons
from tomwer.core.process.stitching.nabustitcher import StitcherTask
from tomwer.io.utils.tomoobj import get_tomo_objs_instances
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.gui.stitching.StitchingWindow import ZStitchingWindow as _ZStitchingWindow
from tomwer.gui.stitching.StitchingWindow import YStitchingWindow as _YStitchingWindow
from tomwer.gui.stitching import action as stitching_action
from tomwer.gui.cluster.slurm import SlurmSettingsWidget
from tomwer.core.scan.scanbase import TomwerScanBase


class MainWidget(qt.QTabWidget):
    DEFAULT_NB_WORKERS = 10

    def __init__(
        self,
        axis: int,
        parent=None,
    ) -> None:
        super().__init__(parent)
        if axis == 0:
            self._stitchingConfigWindow = _ZStitchingWindow(
                parent=self,
                with_configuration_action=False,
            )
        elif axis == 1:
            self._stitchingConfigWindow = _YStitchingWindow(
                parent=self, with_configuration_action=False
            )
        else:
            raise ValueError("stitching is only available along axis 0 and 1")

        self.addTab(self._stitchingConfigWindow, "stitching config")
        settingsClass = SlurmSettingsMode.get_settings_class(
            SlurmSettingsMode.STITCHING
        )
        self._slurmConfig = SlurmSettingsWidget(
            parent=self, n_gpu=settingsClass.N_GPUS_PER_WORKER, jobLimitation=None
        )
        self._slurmConfig.setConfiguration(
            {
                "cpu-per-task": settingsClass.N_CORES_PER_TASK,
                "n_tasks": settingsClass.N_TASKS,
                "n_jobs": settingsClass.N_JOBS,
                "memory": settingsClass.MEMORY_PER_WORKER,
                "partition": settingsClass.PARTITION,
                "n_gpus": settingsClass.N_GPUS_PER_WORKER,
                "job_name": settingsClass.PROJECT_NAME,
                "python_venv": settingsClass.PYTHON_VENV,
            }
        )

        self._stitchingConfigWindow.setCallbackToGetSlurmConfig(
            self._slurmConfig.getConfiguration
        )
        self._stitchingConfigWindow.setCallbackToSetSlurmConfig(
            self._slurmConfig.setConfiguration
        )
        self.addTab(self._slurmConfig, "slurm config")
        # add an option to clearly activate / deactivate slurm config
        slurm_config_idx = self.indexOf(self._slurmConfig)
        self._slurmCB = qt.QCheckBox(self)
        self.tabBar().setTabButton(
            slurm_config_idx,
            qt.QTabBar.LeftSide,
            self._slurmCB,
        )
        self._slurmCB.setChecked(True)

        # set up
        self._slurmConfig.setNWorkers(self.DEFAULT_NB_WORKERS)

    def close(self):
        self._stitchingConfigWindow.close()
        # requested for the waiting plot update
        super().close()

    def keyPressEvent(self, event):
        """
        To shortcut orange and make sure the `F5` <=> refresh stitching preview
        """
        modifiers = event.modifiers()
        key = event.key()

        if key == qt.Qt.Key_F5:
            self._stitchingConfigWindow._trigger_update_preview()
        elif key == qt.Qt.Key_O and modifiers == qt.Qt.KeyboardModifier.ControlModifier:
            self._stitchingConfigWindow._loadSettings()
        elif key == qt.Qt.Key_S and modifiers == qt.Qt.KeyboardModifier.ControlModifier:
            self._stitchingConfigWindow._saveSettings()

    def getStitchingConfiguration(self) -> dict:
        return self._stitchingConfigWindow.getConfiguration()

    def getClusterConfig(self) -> dict:
        return self._slurmConfig.getConfiguration()

    # expose API
    def addTomoObj(self, *args, **kwargs):
        self._stitchingConfigWindow.addTomoObj(*args, **kwargs)

    def setStitchingType(self, stitching_type):
        self._stitchingConfigWindow.setStitchingType(stitching_type)

    def loadSettings(self, config_file):
        self._stitchingConfigWindow._loadSettings(config_file)


class _StitcherThread(qt.QThread):
    DEFAULT_OUTPUT_CONFIG_NAME = "stitching_conf_autosave.conf"

    def __init__(self, parent, stitching_config, cluster_config) -> None:
        super().__init__(parent)
        assert isinstance(stitching_config, dict)
        assert isinstance(cluster_config, dict)
        self._stitching_config = stitching_config
        self._cluster_config = cluster_config

    def save_configuration(self):
        stitching_type = self._stitching_config["stitching"]["type"]
        if "preproc" in stitching_type:
            output_file = self._stitching_config.get("preproc", {}).get("location", "")
            output_folder = os.path.dirname(output_file)
        else:
            output_volume = self._stitching_config.get("postproc", {}).get(
                "output_volume", None
            )
            if output_volume is None:
                output_folder = ""
            else:
                volume = VolumeFactory.create_tomo_object_from_identifier(output_volume)
                output_folder = os.path.dirname(volume.data_url.file_path())

        os.makedirs(output_folder, exist_ok=True)
        generate_nabu_configfile(
            fname=os.path.join(
                output_folder,
                _StitcherThread.DEFAULT_OUTPUT_CONFIG_NAME,
            ),
            default_config=get_default_stitching_config(
                self._stitching_config["stitching"]["type"]
            ),
            comments=True,
            sections_comments=SECTIONS_COMMENTS,
            options_level="advanced",
            prefilled_values=self._stitching_config,
        )

    def run(self):
        self.save_configuration()

        task = StitcherTask(
            inputs={
                "stitching_config": self._stitching_config,
                "cluster_config": self._cluster_config,
                "progress": tqdm(desc="stitching"),
                "serialize_output_data": False,
            },
        )

        task.run()
        print("stitching finished")


class MainWindow(qt.QDialog):
    def __init__(self, axis: int, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())
        # menu
        self._menuBar = qt.QMenuBar(self)
        self.layout().addWidget(self._menuBar)
        self._menu = qt.QMenu("&Stitching")
        self._menuBar.addMenu(self._menu)
        # save / load configuration
        self._loadConfigurationAction = stitching_action.LoadConfigurationAction(
            self, "&Load configuration"
        )
        self._menu.addAction(self._loadConfigurationAction)
        self._saveConfigurationAction = stitching_action.SaveConfigurationAction(
            self, "&Save configuration"
        )
        self._menu.addAction(self._saveConfigurationAction)
        # separator
        self._menu.addSeparator()
        # add tomo object
        self._addTomoObjectAction = stitching_action.AddTomoObjectAction(
            self, "&Add tomo object (volume or NXtomo)"
        )
        self._menu.addAction(self._addTomoObjectAction)

        # main window
        self.setWindowTitle("tomwer z-stitching")
        self._mainWindow = MainWidget(parent=self, axis=axis)
        self.layout().addWidget(self._mainWindow)

        # button
        types = qt.QDialogButtonBox.Apply
        self._buttons = qt.QDialogButtonBox(self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)
        self._buttons.button(qt.QDialogButtonBox.Apply).setText("Launch stitching")

        # connect signal / slot
        self._buttons.button(qt.QDialogButtonBox.Apply).clicked.connect(self.accept)
        self._loadConfigurationAction.triggered.connect(
            functools.partial(
                self._mainWindow._stitchingConfigWindow._loadSettings, file_path=None
            )
        )
        self._saveConfigurationAction.triggered.connect(
            functools.partial(
                self._mainWindow._stitchingConfigWindow._saveSettings, file_path=None
            )
        )
        self._addTomoObjectAction.triggered.connect(self._callbackAddTomoObj)

    def _callbackAddTomoObj(self, *args, **kwargs):
        """move interface to the z-ordered list and call the 'add tomo obj' callback"""
        orderedListWidget = (
            self._mainWindow._stitchingConfigWindow._widget._mainWidget._axisOrderedList
        )
        self._mainWindow._stitchingConfigWindow._widget._mainWidget.setCurrentWidget(
            orderedListWidget
        )
        orderedListWidget._callbackAddTomoObj()

    def close(self):
        self._mainWindow.close()
        # requested for the waiting plot update
        super().close()

    def reject(self):
        self.close()
        super().reject()

    def accept(self):
        self.process_stitching()

    def process_stitching(self):
        self._processingThread = _StitcherThread(
            parent=self,
            stitching_config=self.getStitchingConfiguration(),
            cluster_config=self.getClusterConfig(),
        )
        self._processingThread.start()

    def disableSlurmconfig(self):
        self._mainWindow._slurmCB.setChecked(False)
        self._mainWindow._slurmCB.setCheckable(False)

        slurm_config_idx = self._mainWindow.indexOf(self._mainWindow._slurmConfig)

        self._mainWindow.setTabEnabled(
            slurm_config_idx,
            False,
        )
        self._mainWindow.setTabToolTip(
            slurm_config_idx,
            "not available because unable to find slurm command (computer is probably not a slurm client ?",
        )

    # expose API
    def addTomoObj(self, *args, **kwargs):
        self._mainWindow.addTomoObj(*args, **kwargs)

    def getClusterConfig(self) -> dict:
        if self._mainWindow._slurmCB.isChecked():
            return self._mainWindow.getClusterConfig()
        else:
            return {}

    def getStitchingConfiguration(self) -> dict:
        return self._mainWindow.getStitchingConfiguration()

    def setStitchingType(self, stitching_type):
        self._mainWindow.setStitchingType(stitching_type)

    def loadSettings(self, config_file: str):
        self._mainWindow.loadSettings(config_file)


def main(argv, stitcher_name: str, stitching_axis: int, logger):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "tomo_objs",
        help="All tomo objects to be stitched together",
        nargs="*",
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Set logging system in debug mode",
    )

    parser.add_argument(
        "--config",
        "--config-file",
        dest="config_file",
        default=None,
        help="Provide stitching configuration file to load parameters from it",
    )
    parser.add_argument(
        "--use-opengl-plot",
        help="Use OpenGL for plots (instead of matplotlib)",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--check-scans",
        help="If True will check scans before adding them. This check scan validity (virtual dataset contains data...)",
        action="store_true",
        default=False,
    )
    options = parser.parse_args(argv[1:])

    if options.use_opengl_plot:
        silx.config.DEFAULT_PLOT_BACKEND = "gl"
    else:
        silx.config.DEFAULT_PLOT_BACKEND = "matplotlib"

    if options.debug:
        logging.root.setLevel(logging.DEBUG)

    increase_max_number_file()

    global app  # QApplication must be global to avoid seg fault on quit
    app = qt.QApplication.instance() or qt.QApplication(["tomwer"])
    splash = getMainSplashScreen()
    qt.QApplication.processEvents()

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler

    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catch
    timer.timeout.connect(lambda: None)

    window = MainWindow(axis=stitching_axis)
    window.setWindowFlags(qt.Qt.Window)
    window.setWindowTitle(stitcher_name)
    window.setWindowIcon(icons.getQIcon("tomwer"))

    window.show()
    from sluurp.utils import has_sbatch_available

    # load configuration is some provided
    if options.config_file is not None:
        window.loadSettings(options.config_file)

    if not has_sbatch_available():
        window.disableSlurmconfig()

    tomo_objs, (has_scans, has_vols) = get_tomo_objs_instances(options.tomo_objs)
    for tomo_obj in tomo_objs:
        if isinstance(tomo_obj, TomwerScanBase):
            tomo_obj.set_check_behavior(
                run_check=options.check_scans
            )  # speed up processing
        window.addTomoObj(tomo_obj=tomo_obj)
    if has_scans and has_vols:
        logger.warning(
            "seems like you have both volumes and scan on your inputs. Unable to stitch the two at the same time"
        )
    elif has_scans:
        if stitching_axis == 0:
            window.setStitchingType(StitchingType.Z_PREPROC)
        elif stitching_axis == 1:
            window.setStitchingType(StitchingType.Y_PREPROC)
        else:
            raise ValueError(
                f"stitching on scans is not possible along the axis {stitching_axis} (must be 0 or 1)"
            )
    elif has_vols:
        if stitching_axis == 0:
            window.setStitchingType(StitchingType.Z_POSTPROC)
        else:
            raise ValueError(
                f"stitching on volumes is not possible along the axis {stitching_axis} (must be 0). Should be possible in theory. Please contact us so we can have a dataset and test it"
            )

    window.setAttribute(qt.Qt.WA_DeleteOnClose)
    splash.finish(window)
    exit(app.exec_())


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.closeAllWindows()  # needed because get a waiting thread behind
    qt.QApplication.quit()
