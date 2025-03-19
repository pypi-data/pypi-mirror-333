# coding: utf-8

"""
This module analyze headDir data directory to detect scan to be reconstructed
"""
from __future__ import annotations

import logging
import os
import subprocess
from glob import glob

from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.signal import Signal

from .status import OBSERVATION_STATUS

logger = logging.getLogger(__name__)

try:
    from tomwer.synctools.rsyncmanager import RSyncManager

    has_rsync = False
except ImportError:
    logger.warning("rsyncmanager not available")
    has_rsync = True


"""
Useful tools
"""


class _DataWatcherProcess:
    """
    DataWatcherProcess is the process managing the observation of acquisition.
    Since we want to loop infinitly on a root folder we have to ignore the
    folder we previously detected. Otherwise if those folders are not removed
     we will loop infinitly. That is why we now have the ignoredFolders
     parameter.

    Example of usage of srcPattern and destPattern:

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

    :param  dataDir: Root directory containing data
    :param  waitXML: if True then we will be waiting for the XML of
        the acquisition to be writted. Otherwise we will look for the .info
        file and wait until all file will be copied
    :param srcPattern: the pattern to change by destPattern.
    :param destPattern: the pattern that will replace srcPattern in the
        scan path
    :param list ignoredFolders: the list of folders to ignored on parsing
                                 (them and sub folders)
    """

    sigNbDirExplored = Signal(int)
    """Signal emitted to notice the number of directory at the top level"""
    sigAdvanceExploration = Signal(int)
    """signal emitted each time a top level directory is parsed"""
    sigNewObservation = Signal(tuple)
    """used to signal a new step on the acquisition (first element of the tuple
        should be on eof OBSERVATION_STATUS, second element can be extra
        information to be displayed )"""

    sigNewInformation = Signal(str)
    """Signal used to communicate some random information (will originally be
        displayed in DataWatcherOW)"""

    INITIAL_STATUS = "not processing"

    def __init__(
        self,
        dataDir: str,
        srcPattern: str | None = None,
        destPattern: str | None = None,
    ):
        super().__init__()
        self.RootDir = os.path.abspath(dataDir)
        self.parsing_dir = os.path.abspath(dataDir)
        self.oldest = 0
        self.curdir = ""
        self.scan_name = ""
        self.scan_completed = False
        self.reconstructed = False
        self.status = self.INITIAL_STATUS
        """contains the step of acquisition we are looking for and the
        status on this step"""
        self.quitting = False
        self._removed = None

        srcPatternInvalid = srcPattern not in [None, ""] and not os.path.isdir(
            srcPattern
        )
        destPatternInvalid = destPattern not in [None, ""] and not os.path.isdir(
            destPattern
        )

        if srcPatternInvalid or destPatternInvalid:
            srcPattern = None
            destPattern = None

        self.srcPattern = srcPattern if destPattern is not None else None
        self.destPattern = destPattern if srcPattern is not None else None

    def _setStatus(self, status, info=None):
        assert status in OBSERVATION_STATUS
        self.status = status
        if info is None:
            self.sigNewObservation.emit((status,))
        else:
            self.sigNewObservation.emit((status, info))

    def _removeAcquisition(self, scanID, reason):
        raise NotImplementedError("Base class")

    def dir_explore(self):
        """
        Explore directory tree until valid .file_info_ext file is found.
        Tree explored by ascending order relative to directory date depending
        self.oldest

        :return: True if the acquisition as started else False
        """
        self.status = "start acquisition"

    def _sync(self):
        """Start to copy files from /lbsram/path to path if on lbsram

        :return: True if the synchronization starts
        """
        if has_rsync:
            return False

        if self.srcPattern:
            assert os.path.isdir(self.srcPattern) or self.srcPattern == ""
            assert os.path.isdir(self.destPattern) or self.destPattern == ""
            if self.RootDir.startswith(self.srcPattern):
                source = os.path.join(self.RootDir, self.parsing_dir)
                target = source.replace(self.srcPattern, self.destPattern, 1)
                info = f"Start synchronization between {source} and {target}"
                self.sigNewInformation.emit(info)

                target_dirname = os.path.dirname(target)
                # check if a synchronization is already running, avoid
                # duplication
                try:
                    if not RSyncManager().has_active_sync(source, target_dirname):
                        RSyncManager().sync_file(source, target_dirname)
                except subprocess.TimeoutExpired:
                    # if time out expired, do the synchronization anyway
                    RSyncManager().sync_file(source, target_dirname)
                return True
        else:
            return False

    def is_data_complete(self):
        """
        Check that data file is found and complete

        :return: - 0 if the acquisition is no finished
                 - 1 if the acquisition is finished
                 - -1 observation has been stopped
        """
        raise NotImplementedError("_DataWatcherProcess is a pure virtual class")

    def getCurrentDir(self):
        """Return the current dircetory parsed absolute path"""
        return os.path.join(self.RootDir, self.parsing_dir)

    def _isScanDirectory(self, directory):
        if EDFTomoScan.directory_contains_scan(
            directory, src_pattern=self.srcPattern, dest_pattern=self.destPattern
        ):
            scan = EDFTomoScan(directory)

            # keep compatibility EDF: get detector
            aux = directory.split(os.path.sep)
            infoname = os.path.join(directory, aux[-1] + EDFTomoScan.INFO_EXT)

            if self.srcPattern:
                infoname = infoname.replace(self.srcPattern, self.destPattern, 1)
            """
            assume 1st it is standard info filename
            """
            gd = glob(os.path.join(directory, infoname))
            if len(gd) == 0:
                """
                To detect if it is PCO like, check if info filename contains 0000
                """
                gd = glob(os.path.join(directory, EDFTomoScan.INFO_EXT))
                if len(gd) > 0:
                    self.detector = "Dimax"
        else:
            return False

        if scan.is_abort(src_pattern=self.srcPattern, dest_pattern=self.destPattern):
            self._removeAcquisition(
                scanID=directory, reason="acquisition aborted by the user"
            )

        # TODO: add a scan.get_status() function to get the acquisition status?
        self._setStatus("started")
        return True

    def is_abort(self):
        raise NotImplementedError("Base class")


class _DataWatchEmpty(_DataWatcherProcess):
    """A data watcher which just look under sub directories"""

    def is_data_complete(self):
        return False

    def _removeAcquisition(self, scanID, reason):
        pass
