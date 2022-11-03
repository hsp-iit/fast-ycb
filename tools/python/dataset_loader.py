#===============================================================================
#
# Copyright (C) 2022 Istituto Italiano di Tecnologia (IIT)
#
# This software may be modified and distributed under the terms of the
# GPL-2+ license. See the accompanying LICENSE file for details.
#
#===============================================================================

import cv2
import json
import numpy
import os
import struct


class Loader():

    def __init__(self, path, object_folder):
        """Constructor."""

        self._path = os.path.join(path, object_folder)
        self._number_frames = None

        self._load_number_frames()
        self._load_camera_parameters()


    def _load_number_frames(self):
        """Load the total number of frames."""

        self._number_frames = sum(1 for line in open(os.path.join(self._path, 'data.txt')))


    def _load_camera_parameters(self):
        """Load the camera parameters."""

        self._camera_parameters = json.load(open(os.path.join(self._path, 'cam_K.json')))


    def _is_valid_frame(self, number):
        """Check if the frame with frame number 'number' does exists."""

        return number < self._number_frames


    def get_number_frames(self):
        """Get the total number of frames."""

        return self._number_frames


    def get_camera_parameters(self):
        """Get the camera parameterss."""

        return self._camera_parameters


    def get_rgb(self, number):
        """Get the rgb frame given the frame number."""

        if not self._is_valid_frame(number):
            raise ValueError('The frame with frame number ' + str(number) + ' does not exist.')

        return cv2.imread(os.path.join(self._path, 'rgb', str(number) + '.png'))


    def get_depth(self, number):
        """Get the depth frame given the frame number."""

        if not self._is_valid_frame(number):
            raise ValueError('The frame with frame number ' + str(number) + ' does not exist.')

        with open(os.path.join(self._path, 'depth', str(number) + '.float'), 'rb') as f:
            width, = struct.unpack('=Q', f.read(8))
            height, = struct.unpack('=Q', f.read(8))
            depth = numpy.reshape \
                    (
                        numpy.array(struct.unpack('f' * width * height, f.read())),
                        (height, width)
                    )

        return depth


    def get_optical_flow(self, number):
        """Get the flow frame given the frame number."""

        type_map = {cv2.CV_32FC2 : 'f', cv2.CV_16SC2 : 'h'}
        type_scaling = {cv2.CV_32FC2 : 1.0, cv2.CV_16SC2 : float(2 ** 5)}

        if not self._is_valid_frame(number):
            raise ValueError('The frame with frame number ' + str(number) + ' does not exist.')

        with open(os.path.join(self._path, 'optical_flow/nvof_1_slow', str(number) + '.float'), 'rb') as f:
            frame_type, = struct.unpack('i', f. read(4))
            width, = struct.unpack('=Q', f.read(8))
            height, = struct.unpack('=Q', f.read(8))
            flow = numpy.reshape \
                (
                    numpy.array(struct.unpack(type_map[frame_type] * width * height * 2, f.read())),
                    (height, width, 2)
                ) / type_scaling[frame_type]

        return flow


    def get_mask(self, number):
        """Get the mask frame given the frame number."""

        if not self._is_valid_frame(number):
            raise ValueError('The frame with frame number ' + str(number) + ' does not exist.')

        return cv2.imread(os.path.join(self._path, 'masks', 'gt', self._object_name + '_' + str(number) + '.png'))
