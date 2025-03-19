import os

import numpy
from nxtomo.application.nxtomo import NXtomo
from scipy.ndimage import shift as shift_scipy
from silx.image.phantomgenerator import PhantomGenerator
from nxtomo.nxobject.nxdetector import ImageKey

from tomwer.core.scan.nxtomoscan import NXtomoScan
from nxtomo.utils.transformation import DetYFlipTransformation, DetZFlipTransformation


def create_scans_z_series(
    output_dir,
    z_positions_m,
    x_positions_m=None,
    pixel_size=10e-6,
    n_proj=20,
    raw_frame_width=100,
    final_frame_width=100,
    shifts=None,
    z_rois=None,
    flip_lr: bool = False,
    flip_ud: bool = False,
):
    """
    :param Optional tuple: shift to be applied on the 2D frame
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    frame = (
        PhantomGenerator.get2DPhantomSheppLogan(n=raw_frame_width).astype(numpy.float32)
        * 256.0
    )
    if x_positions_m is None:
        x_positions_m = [None] * len(z_positions_m)
    if shifts is None:
        shifts = [None] * len(z_positions_m)
    if z_rois is None:
        z_rois = [None] * len(z_positions_m)
    scans = []
    for i_frame, (z_pos, x_pos, z_roi, shift) in enumerate(
        zip(z_positions_m, x_positions_m, z_rois, shifts)
    ):
        nx_tomo = NXtomo()
        if z_pos is not None:
            nx_tomo.sample.z_translation = [z_pos] * n_proj
        if x_pos is not None:
            nx_tomo.sample.x_translation = [x_pos] * n_proj
        nx_tomo.sample.rotation_angle = numpy.linspace(
            0, 180, num=n_proj, endpoint=False
        )
        nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION] * n_proj
        if pixel_size is not None:
            if isinstance(pixel_size, (tuple, list)):
                y_pix_size, x_pix_size = pixel_size
            else:
                y_pix_size, x_pix_size = pixel_size, pixel_size
            nx_tomo.instrument.detector.x_pixel_size = x_pix_size
            nx_tomo.instrument.detector.y_pixel_size = y_pix_size
        nx_tomo.instrument.detector.distance = 2.3
        nx_tomo.energy = 19.2
        nx_tomo.instrument.detector.transformations.add_transformation(
            DetYFlipTransformation(flip=flip_ud)
        )
        nx_tomo.instrument.detector.transformations.add_transformation(
            DetZFlipTransformation(flip=flip_lr)
        )

        if shift is not None:
            sub_frame = shift_scipy(
                input=frame.copy(), shift=shift, order=1, mode="constant"
            )[:final_frame_width]
        else:
            sub_frame = frame
        if z_roi is not None:
            roi_start, roi_end = z_roi
            sub_frame = sub_frame[roi_start:roi_end]
        else:
            sub_frame = sub_frame
        if flip_lr:
            sub_frame = numpy.fliplr(sub_frame)
        if flip_ud:
            sub_frame = numpy.flipud(sub_frame)
        nx_tomo.instrument.detector.data = numpy.asarray([sub_frame] * n_proj)

        file_path = os.path.join(output_dir, f"nxtomo_{i_frame}.nx")
        entry = f"entry000{i_frame}"
        nx_tomo.save(file_path=file_path, data_path=entry)
        scans.append(NXtomoScan(scan=file_path, entry=entry))

    return scans
