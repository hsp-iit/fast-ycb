#===============================================================================
#
# Copyright (C) 2022 Istituto Italiano di Tecnologia (IIT)
#
# This software may be modified and distributed under the terms of the
# GPL-2+ license. See the accompanying LICENSE file for details.
#
#===============================================================================

import cv2
import numpy
import open3d as o3d
import sys
from dataset_loader import Loader


def eval_point_cloud(depth, rgb, max_depth, camera_parameters):

    width = camera_parameters['width']
    height = camera_parameters['height']
    fx = float(camera_parameters['fx'])
    fy = float(camera_parameters['fy'])
    cx = float(camera_parameters['cx'])
    cy = float(camera_parameters['cy'])

    image_x_z = numpy.zeros((height, width), dtype = numpy.float32)
    image_y_z = numpy.zeros((height, width), dtype = numpy.float32)
    for v in range(height):
        for u in range(width):
            image_x_z[v, u] = (u - cx) / fx
            image_y_z[v, u] = (v - cy) / fy

    valid_depth = depth < max_depth
    coords_z = depth[valid_depth]
    coords_x_z = image_x_z[valid_depth]
    coords_y_z = image_y_z[valid_depth]

    rgb_fixed = rgb.copy()
    rgb_fixed = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    colors = rgb_fixed[valid_depth]

    cloud = numpy.zeros((coords_z.shape[0], 3), dtype = numpy.float32)
    cloud[:, 0] = coords_x_z * coords_z
    cloud[:, 1] = coords_y_z * coords_z
    cloud[:, 2] = coords_z

    return cloud, colors


def add_point_cloud(name, cloud, colors, size, scene):

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(cloud)
    point_cloud.colors = o3d.utility.Vector3dVector(colors / 255.0)

    material = o3d.visualization.rendering.MaterialRecord()
    material.shader = 'defaultUnlit'
    material.point_size = size

    scene.add_geometry(name, point_cloud, material)


def main():
    fastycb_path = './'
    object_folder = sys.argv[1]
    loader = Loader(path = fastycb_path, object_name = object_folder)

    # Load camera parameters
    camera_parameters = loader.get_camera_parameters()

    # Show sample point cloud for a given frame index
    index = 1
    rgb = loader.get_rgb(index)
    depth = loader.get_depth(index)
    max_depth = 1.0
    cloud, cloud_colors = eval_point_cloud(depth, rgb, max_depth, camera_parameters)

    try:
        app = o3d.visualization.gui.Application.instance
        app.initialize()

        window = app.create_window("Point cloud viewer", 1024, 768)

        widget3d = o3d.visualization.gui.SceneWidget()
        widget3d.scene = o3d.visualization.rendering.Open3DScene(window.renderer)
        widget3d.scene.set_background([1.0, 1.0, 1.0, 1.0])
        window.add_child(widget3d)

        add_point_cloud('cloud', cloud, cloud_colors, 2, widget3d.scene)
        widget3d.setup_camera(60, widget3d.scene.bounding_box, [0, 0, 0])

        app.run()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
