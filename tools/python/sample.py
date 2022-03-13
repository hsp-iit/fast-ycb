#===============================================================================
#
# Copyright (C) 2022 Istituto Italiano di Tecnologia (IIT)
#
# This software may be modified and distributed under the terms of the
# GPL-2+ license. See the accompanying LICENSE file for details.
#
#===============================================================================

from dataset_loader import Loader
import cv2
import imgviz
import numpy
import sys


def main():
    fastycb_path = './'
    object_folder = sys.argv[1]
    loader = Loader(path = fastycb_path, object_folder = object_folder)

    # Print useful information
    print('# frames: ', loader.get_number_frames())
    print('camera parameters')
    print(loader.get_camera_parameters())

    # Show sample RGB, depth and optical flow frames
    for i in range(500, min(1000, loader.get_number_frames())):
        # Get all frames
        rgb = loader.get_rgb(i)
        depth = loader.get_depth(i)
        flow = loader.get_optical_flow(i)

        # Render depth and optical flow using RGB colors
        depth_render = imgviz.depth2rgb(depth, min_value = 0.3, max_value = 1.5, colormap = 'rainbow')
        flow_render = imgviz.flow2rgb(flow)

        # Render RGB, depth and optical flow in a single frame
        scale = 0.4
        height = int(rgb.shape[0] * scale)
        width = int(rgb.shape[1] * scale)
        render = numpy.empty([height, 3 * width, 3], 'uint8')

        render[:, : width] = cv2.resize(rgb, (width, height))
        render[:, width : 2 * width] = cv2.resize(depth_render, (width, height))
        render[:, 2 * width : 3 * width] = cv2.resize(flow_render, (width, height))

        cv2.imshow('', render)
        cv2.waitKey(33)


if __name__ == '__main__':
    main()
