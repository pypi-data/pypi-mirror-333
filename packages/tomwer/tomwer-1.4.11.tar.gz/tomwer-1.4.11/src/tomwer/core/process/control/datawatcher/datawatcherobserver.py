from __future__ import annotations

import logging
import os
import threading
import time
from collections import OrderedDict
from fnmatch import fnmatch

import h5py

from tomwer.core.process.control.datawatcher import status as datawatcherstatus
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.utils.threads import LoopThread

from .datawatcherprocess import _DataWatchEmpty
from .edfdwprocess import (
    _DataWatcherProcessParseInfo,
    _DataWatcherProcessUserFilePattern,
    _DataWatcherProcessXML,
)
from .hdf5dwprocess import _BlissScanWatcherProcess, _DataWatcherProcessHDF5

logger = logging.getLogger(__name__)


class _DataWatcherStaticObserverMixIn:
    def __init__(
        self,
        scanID,
        obsMethod,
        srcPattern: str | None,
        destPattern: str | None,
        patternObs: str | None,
        observationRegistry,
    ):
        """

        :param scanID: path to the scan
        :param obsMethod: method fo rdetecting end of acquisition
        :param srcPattern:
        :param destPattern:
        :param patternObs:
        :param observationRegistry: what registry the observation should update
        """
        self.obsMethod = obsMethod
        self.srcPattern = srcPattern
        self.destPattern = destPattern
        self.patternObs = patternObs
        """The pattern to use for the DET_END_USER_ENTRY method"""
        self.setDirToObserve(scanID)
        self.dataWatcherProcess = self._getDataWatcherProcess()
        self.status = "not processing"
        self.observationRegistry = observationRegistry
        self.file_name_pattern = None

    def setProperties(self, properties):
        assert isinstance(properties, dict)
        if "scan" in properties:
            self.setDirToObserve(properties["scan"])

    def setDirToObserve(self, directory):
        self.path = directory
        if hasattr(self, "dataWatcherProcess") and self.dataWatcherProcess:
            self.dataWatcherProcess.RootDir = directory
            self.dataWatcherProcess.parsing_dir = ""

    def quit(self):
        if self.dataWatcherProcess is not None:
            self.dataWatcherProcess.quitting = True

    def run(self):
        look_for_hdf5_file = self.obsMethod in (
            datawatcherstatus.BLISS_SCAN_END,
            datawatcherstatus.NXtomo_END,
        )

        if not look_for_hdf5_file and not os.path.isdir(self.path):
            logger.info("can't observe %s, not a directory" % self.path)
            self.status = "failure"
            if self.observationRegistry:
                self.observationRegistry._updateStatus(
                    status=datawatcherstatus.OBSERVATION_STATUS[self.status],
                    scan=self.path,
                )
            self.validation = -1
            return

        if self.dataWatcherProcess.is_abort():
            if self.status != "aborted":
                logger.info("Acquisition %s has been aborted" % self.path)
                self.dataWatcherProcess._removeAcquisition(
                    scanID=self.path, reason="acquisition aborted by the user"
                )

                self.status = "aborted"
            if self.observationRegistry:
                self.observationRegistry._updateStatus(
                    status=datawatcherstatus.OBSERVATION_STATUS[self.status],
                    scan=self.path,
                )
            self.validation = -2
            return

        dataComplete = self.dataWatcherProcess.is_data_complete()

        if dataComplete is True:
            self.status = "acquisition ended"
            if self.observationRegistry:
                self.observationRegistry._updateStatus(
                    status=datawatcherstatus.OBSERVATION_STATUS[self.status],
                    scan=self.path,
                )
            self.validation = 1
        else:
            self.status = "waiting for acquisition ending"
            if self.observationRegistry:
                self.observationRegistry._updateStatus(
                    status=datawatcherstatus.OBSERVATION_STATUS[self.status],
                    scan=self.path,
                )
            self.validation = 0
        return

    def _getDataWatcherProcess(self):
        if self.obsMethod == datawatcherstatus.DET_END_XML:
            return _DataWatcherProcessXML(
                dataDir=self.path,
                srcPattern=self.srcPattern,
                destPattern=self.destPattern,
            )
        elif self.obsMethod == datawatcherstatus.PARSE_INFO_FILE:
            return _DataWatcherProcessParseInfo(
                dataDir=self.path,
                srcPattern=self.srcPattern,
                destPattern=self.destPattern,
            )
        elif self.obsMethod == datawatcherstatus.DET_END_USER_ENTRY:
            return _DataWatcherProcessUserFilePattern(
                dataDir=self.path,
                srcPattern=self.srcPattern,
                destPattern=self.destPattern,
                pattern=self.patternObs,
            )
        elif self.obsMethod == datawatcherstatus.BLISS_SCAN_END:
            return _BlissScanWatcherProcess(
                dataDir=self.path,
                srcPattern=self.srcPattern,
                destPattern=self.destPattern,
            )
        elif self.obsMethod == datawatcherstatus.NXtomo_END:
            return _DataWatcherProcessHDF5(
                dataDir=self.path,
                srcPattern=self.srcPattern,
                destPattern=self.destPattern,
            )
        else:
            raise ValueError("requested observation method not recognized")

    def setSourceToDestinationPatterns(self, srcPattern, destPattern):
        """set the patterns to replace strings sequence in directories path.

        For example during acquisition in md05 acquisition files are stored
        in /lbsram/data/visitor/x but some information (as .info) files are
        stored in /data/visitor/x.
        So we would like to check information in both directories.
        Furthermore we would like that all file not in /data/visitor/x will be
        copied as soon as possible into /data/visitor/x (using RSyncManager)

        To do so we can define a srcPattern ('/lbsram' in our example) and
        destPattern : a string replacing to srcPattern in order to get both
        repositories. ('' in out example)
        If srcPattern or destPattern are setted to None then we won't apply
        this 'two directories' synchronization and check

        :param srcPattern: the pattern to change by destPattern.
        :param destPattern: the pattern that will replace srcPattern in the
            scan path
        """
        self.srcPattern = srcPattern
        self.destPattern = destPattern

    def setUnixFileNamePattern(self, pattern):
        self.file_name_pattern = pattern

    def setObservationMethod(self, obsMeth: str | None, info=None):
        """
        Set if we are looking for the .xml file

        :param obsMeth:
        :param info: some extra information needed for some observation
                          method
        """
        assert info is None or type(info) is dict
        assert type(obsMeth) in (tuple, str)
        if type(obsMeth) is str:
            self.obsMethod = obsMeth
            if self.obsMethod == datawatcherstatus.DET_END_USER_ENTRY:
                assert "pattern" in info
                self.patternObs = info["pattern"]
            else:
                self.patternObs = None
        else:
            assert len(obsMeth) > 0
            assert type(obsMeth[0]) is str
            self.obsMethod = obsMeth[0]
            if self.obsMethod == datawatcherstatus.DET_END_USER_ENTRY:
                assert len(obsMeth) == 2
                assert type(obsMeth[1]) is dict
                assert "pattern" in obsMeth[1]
                self.patternObs = obsMeth[1]["pattern"]
            else:
                self.patternObs = None


class _DataWatcherStaticObserver(_DataWatcherStaticObserverMixIn, threading.Thread):
    """Observe one specific directory and signal when the state of this
    directory change"""

    def __init__(
        self,
        scanID,
        obsMethod,
        srcPattern,
        destPattern,
        patternObs,
        observationRegistry,
    ):
        threading.Thread.__init__(self)
        _DataWatcherStaticObserverMixIn.__init__(
            self,
            scanID=scanID,
            obsMethod=obsMethod,
            srcPattern=srcPattern,
            destPattern=destPattern,
            patternObs=patternObs,
            observationRegistry=observationRegistry,
        )


class _DataWatcherObserver_MixIn:
    """Thread launching the data watcher process (observation of acquisition)

    :param headDir: the root dir to make to fin dacquisition
    :param time_between_loops: seconds between observation threads
    :param startByOldest: if True then we parse folder from the oldest to
        the newest
    :param funcAdvancementHandler: handlers of the signals sended by data
                                   watcher (one for sigNbDirExplored and one
                                   for sigAdvanceExploration)
    :param obsMethod: is True then will the creation of the xml file will
        notice the end of the acquisition. Otherwise we will look for .info
        file and for all .edf file to be copied
    :param srcPattern: see data watcher
    :param destPattern: see data watcher
    """

    latestScanReady = []

    def __init__(
        self,
        obsMethod,
        time_between_loops,
        observationClass,
        headDir: str | None = None,
        startByOldest=False,
        srcPattern: str | None = None,
        destPattern: str | None = None,
        ignoredFolders: str | None = None,
        file_name_pattern: str | None = None,
    ):
        self.observations = observationClass()
        self.observations.ignoredFolders = (
            [] if ignoredFolders is None else ignoredFolders
        )
        """dict of observer on one specific scan. Key is the directory,
        value the :class:`DataWatcherFixObserver`"""
        self.setHeadFolder(headDir)
        self.setObservationMethod(obsMethod)
        self.srcPattern = srcPattern
        self.destPattern = destPattern
        self._file_name_pattern = file_name_pattern
        self.dataWatcherProcess = None
        self._patternObs = None
        """The pattern to use for the DET_END_USER_ENTRY method"""
        self.lock = threading.Lock()
        self.restartEvent = None
        self._firstRun = True

    @property
    def file_name_pattern(self) -> str | None:
        return self._file_name_pattern

    @file_name_pattern.setter
    def file_name_pattern(self, pattern: str | None):
        if pattern is None or pattern.lstrip(" ").rstrip(" ") == "":
            self._file_name_pattern = None
        else:
            self._file_name_pattern = pattern.lstrip(" ").rstrip(" ")

    def resetObservations(self):
        self.observations.reset()

    def registerRestartProcess(self, event):
        self.restartEvent = event

    def run(self):
        look_for_hdf5_file = self.obsMethod in (
            datawatcherstatus.BLISS_SCAN_END,
            datawatcherstatus.NXtomo_END,
        )

        def process_observations(file_path):
            do_observation = (
                self.observations.isObserving(file_path) is False
                and (
                    (look_for_hdf5_file and h5py.is_hdf5(file_path))
                    or (self.dataWatcherProcess._isScanDirectory(file_path))
                )
                and file_path not in self.observations.ignoredFolders
            )
            if (
                do_observation
                and self.file_name_pattern is not None
                and not fnmatch(os.path.basename(file_path), self.file_name_pattern)
            ):
                do_observation = False
            if do_observation:
                # do the observation
                self.observe(file_path)

            if os.path.isdir(file_path):
                try:
                    for f in os.listdir(file_path):
                        full_file_path = os.path.join(file_path, f)
                        if os.path.isdir(full_file_path) or (
                            look_for_hdf5_file and h5py.is_hdf5(full_file_path)
                        ):
                            # parse files to check if some observations should be done
                            process_observations(full_file_path)
                except Exception:
                    pass

        if self._firstRun or (
            self.restartEvent is not None and self.restartEvent.isSet()
        ):
            self._firstRun = False
            if self.restartEvent:
                self.restartEvent.clear()

            if not os.path.isdir(self.headDir):
                logger.warning("can't observe %s, not a directory" % self.headDir)
                return
            self._check_scans_ready()  # pylint: disable=E1101
            self.dataWatcherProcess = self._getDataWatcherProcess()
            process_observations(self.headDir)
            self._processObservation()
            self._check_scans_ready()  # pylint: disable=E1101
        else:
            time.sleep(0.5)

    def _processObservation(self):
        threads = list(self.observations.dict.values())
        for thread in threads:
            thread.start()

    def quit(self):
        threads = list(self.observations.dict.values())
        for thread in threads:
            thread.quitting = True

        if self.dataWatcherProcess is not None:
            self.dataWatcherProcess.quitting = True
            self.lastObsDir = None

    def setUnixFileNamePattern(self, pattern):
        self.file_name_pattern = pattern

    def setObservationMethod(self, obsMeth, info=None):
        """
        Set if we are looking for the .xml file from .edf observation or any
        .hdf5 file

        :param or tuple obsMeth:
        :param info: some extra information needed for some observation
                          method
        """
        assert info is None or type(info) is dict
        assert type(obsMeth) in (tuple, str)
        if type(obsMeth) is str:
            self.obsMethod = obsMeth
            if self.obsMethod == datawatcherstatus.DET_END_USER_ENTRY:
                assert "pattern" in info
                self._patternObs = info["pattern"]
            else:
                self._patternObs = None
        else:
            assert len(obsMeth) > 0
            assert type(obsMeth[0]) is str
            self.obsMethod = obsMeth[0]
            if self.obsMethod == datawatcherstatus.DET_END_USER_ENTRY:
                assert len(obsMeth) == 2
                assert type(obsMeth[1]) is dict
                assert "pattern" in obsMeth[1]
                self._patternObs = obsMeth[1]["pattern"]
            else:
                self._patternObs = None

        for _, thread in self.observations.dict.items():
            thread.setObservationMethod(obsMeth, info=info)

    def setHeadFolder(self, headDir):
        assert type(headDir) in (type(None), str)
        self.headDir = headDir

    def setSourceToDestinationPatterns(self, srcPattern, destPattern):
        """set the patterns to replace strings sequence in directories path.

        For example during acquisition in md05 acquisition files are stored
        in /lbsram/data/visitor/x but some information (as .info) files are
        stored in /data/visitor/x.
        So we would like to check information in both directories.
        Furthermore we would like that all file not in /data/visitor/x will be
        copied as soon as possible into /data/visitor/x (using RSyncManager)

        To do so we can define a srcPattern ('/lbsram' in our example) and
        destPattern : a string replacing to srcPattern in order to get both
        repositories. ('' in out example)
        If srcPattern or destPattern are setted to None then we won't apply
        this 'two directories' synchronization and check

        :param srcPattern: the pattern to change by destPattern.
        :param destPattern: the pattern that will replace srcPattern in the
            scan path
        """
        self.srcPattern = srcPattern
        self.destPattern = destPattern
        for _, thread in self.observations.items():
            thread.setSourceToDestinationPatterns(self.srcPattern, self.destPattern)

    def observe(self, scanID):
        self.observations.add(self._getObserver(scanID))  # pylint: disable=E1101

    def cancelObservation(self, scanID):
        if self.observations.isObserving(scanID) is False:
            logger.warning(
                "Can't cancel observation on %s, no observation " "registred" % scanID
            )
            return

        self.observations.ignoredFolders.append(scanID)
        if scanID in self.observations.dict:
            self.observations.remove(self.observations.dict[scanID])

    def isObserve(self, scanID):
        return self.observations.isObserving(scanID)

    def _getDataWatcherProcess(self):
        if self.obsMethod == datawatcherstatus.NXtomo_END:
            return _DataWatcherProcessHDF5(
                dataDir=self.headDir,
                srcPattern=self.srcPattern,
                destPattern=self.destPattern,
            )
        elif self.obsMethod == datawatcherstatus.BLISS_SCAN_END:
            return _BlissScanWatcherProcess(
                dataDir=self.headDir,
                srcPattern=self.srcPattern,
                destPattern=self.destPattern,
            )
        elif EDFTomoScan.directory_contains_scan(
            self.headDir, src_pattern=self.srcPattern, dest_pattern=self.destPattern
        ):
            if self.obsMethod == datawatcherstatus.DET_END_XML:
                return _DataWatcherProcessXML(
                    dataDir=self.headDir,
                    srcPattern=self.srcPattern,
                    destPattern=self.destPattern,
                )
            elif self.obsMethod == datawatcherstatus.PARSE_INFO_FILE:
                return _DataWatcherProcessParseInfo(
                    dataDir=self.headDir,
                    srcPattern=self.srcPattern,
                    destPattern=self.destPattern,
                )
            elif self.obsMethod == datawatcherstatus.DET_END_USER_ENTRY:
                return _DataWatcherProcessUserFilePattern(
                    dataDir=self.headDir,
                    srcPattern=self.srcPattern,
                    destPattern=self.destPattern,
                    pattern=self._patternObs,
                )
        else:
            return _DataWatchEmpty(
                dataDir=self.headDir,
                srcPattern=self.srcPattern,
                destPattern=self.destPattern,
            )


class _DataWatcherObserver(_DataWatcherObserver_MixIn, LoopThread):
    """DataWatcherObserver using Threads"""

    scanReadyEvent = threading.Event()
    """Event set when at least one new scan is found"""

    def __init__(
        self,
        obsMethod,
        time_between_loops,
        observationClass,
        headDir=None,
        startByOldest=False,
        srcPattern=None,
        destPattern=None,
        ignoredFolders=None,
    ):
        LoopThread.__init__(self, time_between_loops=time_between_loops)
        _DataWatcherObserver_MixIn.__init__(
            self,
            obsMethod=obsMethod,
            observationClass=observationClass,
            headDir=headDir,
            startByOldest=startByOldest,
            srcPattern=srcPattern,
            destPattern=destPattern,
            ignoredFolders=ignoredFolders,
            time_between_loops=time_between_loops,
        )

    def _check_scans_ready(self):
        with self.observations.lock:
            if self.observations.scanReadyEvent.isSet():
                for scanReady in self.observations._latestScanReady:
                    self._signalScanReady(scanID=scanReady)
                self.observations.scanReadyEvent.clear()
                self.observations._latestScanReady.clear()

    def _signalScanReady(self, scanID):
        with self.lock:
            self.scanReadyEvent.set()
            self.latestScanReady.append(scanID)

    def _getObserver(self, scanID):
        return _DataWatcherStaticObserver(
            scanID=scanID,
            obsMethod=self.obsMethod,
            srcPattern=self.srcPattern,
            destPattern=self.destPattern,
            patternObs=self._patternObs,
            observationRegistry=self.observations,
        )

    def waitForObservationFinished(self, timeOut=10):
        threads = list(self.observations.dict.values())
        for thread in threads:
            if thread.is_alive():
                thread.join(timeOut)


class _OngoingObservation(object):
    """
    Simple container of observed directory
    """

    scanReadyEvent = threading.Event()
    """Event set a finished acquisition is detected"""
    obsAddedEvent = threading.Event()
    """Event set when an observation is added"""
    obsRemovedEvent = threading.Event()
    """Event set when an observation is removed"""
    obsStatusReceivedEvent = threading.Event()
    """Event set when receiving a new observation status"""

    def __init__(self):
        self.dict = OrderedDict()
        """keys are path, value are observers"""
        self.ignoredFolders = []
        self.lock = threading.Lock()
        self._latestObsEnded = []
        """list of latest observation with scan"""
        self._latestObsAdded = []
        """list of latest removed observations with scan"""
        self._latestObsStatusChanged = []
        """list of latest modify observation with (scan, status)"""
        self._latestScanReady = []
        """list of latest scan ready"""

    def add(self, observer):
        if self.isObserving(observer.path) is False:
            with self.lock:
                assert isinstance(observer, _DataWatcherStaticObserverMixIn)
                self.dict[observer.path] = observer
                self.obsAddedEvent.set()
                self._latestObsEnded.append(observer.path)

    def remove(self, observer):
        assert isinstance(observer, _DataWatcherStaticObserverMixIn)
        if self.isObserving(observer.path) is True:
            # observer.sigStatusChanged.disconnect(self._updateStatus)
            observer.quit()
            del self.dict[observer.path]
            with self.lock:
                self.obsRemovedEvent.set()
                self._latestObsEnded.append(observer.path)

    def _updateStatus(self, status, scan):
        if self.isObserving(scan) is True:
            with self.lock:
                self.obsStatusReceivedEvent.set()
                self._latestObsStatusChanged.append(
                    (scan, datawatcherstatus.DICT_OBS_STATUS[status])
                )
            if status == datawatcherstatus.OBSERVATION_STATUS["acquisition ended"]:
                self._acquisition_ended(scan)
            if status in (
                datawatcherstatus.OBSERVATION_STATUS["failure"],
                datawatcherstatus.OBSERVATION_STATUS["aborted"],
            ):
                observer = self.dict[scan]
                self.remove(observer)

    def _acquisition_ended(self, scanID):
        with self.lock:
            self.ignoredFolders.append(scanID)
            observer = self.dict[scanID]
        self.remove(observer)
        # TODO : disconnect the thread and delete it if finisehd
        #  add the scan to the one to ignore. Those ignore
        # should be removed at each start and stop of the observation
        with self.lock:
            self.scanReadyEvent.set()
            self._latestScanReady.append(scanID)

    def isObserving(self, scan):
        return scan in self.dict

    def reset(self):
        for scanID, observer in self.dict:
            # observer.sigStatusChanged.disconnect(self._updateStatus)
            observer.quit()
        self.dict = {}

    def __len__(self):
        return len(self.dict)

    def __str__(self):
        return str(self.dict.keys())
