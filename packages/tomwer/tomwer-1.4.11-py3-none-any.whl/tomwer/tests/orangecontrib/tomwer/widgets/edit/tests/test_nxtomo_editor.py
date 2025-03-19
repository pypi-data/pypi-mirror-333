import os
import pickle

import numpy
import pytest
from nxtomomill.nexus.nxtomo import NXtomo
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui.utils.testutils import SignalListener
from nxtomo.nxobject.nxdetector import ImageKey

from orangecontrib.tomwer.widgets.edit.NXtomoEditorOW import NXtomoEditorOW
from tomwer.core.process.edit.nxtomoeditor import NXtomoEditorKeys
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.tests.utils import skip_gui_test
from tomwer.gui.utils.qt_utils import QSignalSpy
from tomwer.tests.conftest import qtapp  # noqa F401


def getDefaultConfig() -> dict:
    """return the configuration of the NXtomo editor. First value is the value of the field, second is: is the associated lock button locked or not"""
    return {
        NXtomoEditorKeys.ENERGY: (5.9, False),
        NXtomoEditorKeys.SAMPLE_DETECTOR_DISTANCE: (2.4, True),
        NXtomoEditorKeys.FIELD_OF_VIEW: ("Full", False),
        NXtomoEditorKeys.X_PIXEL_SIZE: (0.023, True),
        NXtomoEditorKeys.Y_PIXEL_SIZE: (0.025, True),
        NXtomoEditorKeys.X_FLIPPED: (True, True),
        NXtomoEditorKeys.Y_FLIPPED: (False, False),
        NXtomoEditorKeys.X_TRANSLATION: (0.0,),
        NXtomoEditorKeys.Z_TRANSLATION: (0.0,),
    }


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
def test_NXtomoEditorOW(
    qtapp,  # noqa F811
    tmp_path,
):
    window = NXtomoEditorOW()
    # test serialization
    window.setConfiguration(getDefaultConfig())
    assert window.getConfiguration() == getDefaultConfig()
    pickle.dumps(window.getConfiguration())

    # test literal dumps
    literal_dumps(window.getConfiguration())

    # test widget automation
    signal_listener = SignalListener()
    window.sigScanReady.connect(signal_listener)
    # set up the widget to define and lock distance, energy and x pixel size
    distance_widget = window.widget.mainWidget._distanceMetricEntry
    distance_widget.setValue(0.6)
    distance_widget.setUnit("mm")
    distance_locker = window.widget.mainWidget._distanceLB
    distance_locker.setLock(True)
    energy_widget = window.widget.mainWidget._energyEntry
    energy_widget.setValue(88.058)
    energy_locker = window.widget.mainWidget._energyLockerLB
    energy_locker.setLock(True)
    x_pixel_widget = window.widget.mainWidget._xPixelSizeMetricEntry
    x_pixel_widget.setValue(45)
    x_pixel_widget.setUnit("nm")
    x_pixel_locker = window.widget.mainWidget._xPixelSizeLB
    x_pixel_locker.setLock(True)

    # 1.0 create nx tomos with raw data
    nx_tomo = NXtomo()
    nx_tomo.instrument.detector.x_pixel_size = (
        0.023  # should be overwrite by the configuration / lock buttons
    )
    nx_tomo.instrument.detector.y_pixel_size = (
        0.025  # should be overwrite by the configuration / lock buttons
    )
    nx_tomo.instrument.detector.field_of_view = "full"
    nx_tomo.instrument.detector.distance = (
        2.4  # should be overwrite by the configuration / lock buttons
    )
    nx_tomo.instrument.detector.x_flipped = (
        False  # should be overwrite by the configuration / lock buttons
    )
    nx_tomo.instrument.detector.y_flipped = True
    nx_tomo.energy = 5.9
    nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION.value] * 12
    nx_tomo.instrument.detector.data = numpy.empty(shape=(12, 10, 10))
    nx_tomo.sample.rotation_angle = numpy.linspace(0, 20, num=12)

    file_path = os.path.join(tmp_path, "nxtomo.nx")
    entry = "entry0000"
    nx_tomo.save(
        file_path=file_path,
        data_path=entry,
    )
    # 2.0 set scan to the nxtomo-editor
    scan = NXtomoScan(file_path, entry)
    waiter = QSignalSpy(window.sigScanReady)
    window.setScan(scan=scan)
    # warning: avoid executing the ewoks task as this will be done
    # automatically (has some field lock). This would create concurrency task
    # and could bring some HDF5 concurrency error
    waiter.wait(5000)
    # 3.0 check results are as expected
    # make sure the scan has been re-emitted
    assert signal_listener.callCount() == 1
    # make sure the edition of the parameters have been done and only those
    overwrite_nx_tomo = NXtomo().load(
        file_path=file_path,
        data_path=entry,
        detector_data_as="as_numpy_array",
    )
    numpy.testing.assert_almost_equal(
        overwrite_nx_tomo.instrument.detector.x_pixel_size.si_value, 45e-9
    )
    assert (
        overwrite_nx_tomo.instrument.detector.y_pixel_size.si_value
        == nx_tomo.instrument.detector.y_pixel_size.si_value
    )
    assert (
        overwrite_nx_tomo.instrument.detector.field_of_view
        == nx_tomo.instrument.detector.field_of_view
    )
    numpy.testing.assert_almost_equal(
        overwrite_nx_tomo.instrument.detector.distance.value, 6.0e-4
    )
    assert (
        overwrite_nx_tomo.instrument.detector.x_flipped
        == True  # is lock to True so should load the value and overwrite it
    )

    assert (
        overwrite_nx_tomo.instrument.detector.y_flipped
        == True  # is not locked and is initially set to False (should load it and ignore overwriting)
    )
    numpy.testing.assert_almost_equal(overwrite_nx_tomo.energy.value, 88.058)
    numpy.testing.assert_array_almost_equal(
        overwrite_nx_tomo.instrument.detector.data,
        nx_tomo.instrument.detector.data,
    )
