<h1 align="center">
  Fast-YCB
</h1>

<p align="center"><img src="https://github.com/hsp-iit/fast-ycb/blob/main/assets/sample.gif" alt="" /></p>

## Description

This is the repository associated to the dataset Fast-YCB presented in the publication [ROFT: Real-Time Optical Flow-Aided 6D Object Pose and Velocity Tracking](https://github.com/hsp-iit/roft).

The dataset is hosted in the [IIT Dataverse](https://dataverse.iit.it/) and it is identified by following [![DOI:10.48557/G2QJDM](http://img.shields.io/badge/DOI-10.48557/G2QJDM-0a7bbc.svg)](https://doi.org/10.48557/G2QJDM).


The dataset contains 6 synthetic sequences comprising objects from the [YCB Model Set](https://www.google.com/search?q=ycb+model+set&oq=ycb+model+set&aqs=chrome..69i57j0i22i30j69i59j69i60l3.2631j0j7&sourceid=chrome&ie=UTF-8). The trajectories of the object are characterized by moderate-to-fast motions and can be used to benchmark 6D object pose tracking algorithms.

The dataset provides RGB, depth, optical flow, segmentation (ground truth and from Mask R-CNN) and 6D object poses (ground truth and from NVIDIA DOPE).

Specifically, the dataset contains (for each object folder):
- `cam_K.json` : a json file containing the camera width, height and intrinsic parameters
- `rgb` : a folder containing rgb frames in `PNG` format
- `depth` : a folder containing depth frames
- `masks/gt` : a folder containing ground truth segmentation masks as binary `PNG` images
- `masks/mrcnn_ycbv_bop_pbr`: a folder containing Mask R-CNN segmentation as binary `PNG images`
- `optical_flow/nvof_1_slow` : a folder containing [NVIDIA NVOF SDK](https://developer.nvidia.com/opticalflow-sdk) optical flow frames
- `dope/poses.txt` : a file containing 6D object poses obtained using [DOPE](https://github.com/NVlabs/Deep_Object_Pose) (these poses assume the [NVDU](https://github.com/NVIDIA/Dataset_Utilities) version of the YCB Model Set meshes)
- `dope/poses_ycb.txt` : as above but assume the original [PoseCNN YCB Model set meshes](https://drive.google.com/file/d/1gmcDD-5bkJfcMKLZb3zGgH_HUFbulQWu/view?usp=sharing)
- `gt/poses.txt` : ground truth 6D poses (NVDU format)
- `gt/poses_ycb.txt` : ground truth 6D poses (PoseCNN YCB Model set format)
- `gt/velocities.txt` : ground truth velocities

### A note on additional sequences

The object folders `003_cracker_box_real` and `006_mustard_bottle_real` contain additional sequences acquired with a real Intel RealSense D415 camera. These are not labeled (i.e. they miss the `masks/gt` and the whole `gt` folders).

## How to obtain the dataset

Download the dataset using:
```console
bash tools/download/download_dataset.sh
```

In order to download the dataset `curl`, `jq`, `unzip` and `zip` are required.

## How to access data

We provide [python](tools/python/sample.py) sample code to access the information contained in the dataset.

```console
pip install -r tools/python/requirements.txt
bash tools/python/sample.py <object_name>
```
where `<object_name>` might be `003_cracker_box`, `004_sugar_box`, `005_tomato_soup_can`, `006_cracker_box`, `009_gelatin_box`, `010_potted_meat_can`.

<p align="center"><img src="https://github.com/hsp-iit/fast-ycb/blob/main/assets/sample_rgbd_flow.png" alt="" /></p>

## Citing Fast-YCB

If you find the Fast-YCB dataset useful, please consider citing the associated publication:

```bibtex
@ARTICLE{9568706,
author={Piga, Nicola A. and Onyshchuk, Yuriy and Pasquale, Giulia and Pattacini, Ugo and Natale, Lorenzo},
journal={IEEE Robotics and Automation Letters},
title={ROFT: Real-Time Optical Flow-Aided 6D Object Pose and Velocity Tracking},
year={2022},
volume={7},
number={1},
pages={159-166},
doi={10.1109/LRA.2021.3119379}
}
```

## Maintainer

This repository is maintained by:

| | |
|:---:|:---:|
| [<img src="https://github.com/xenvre.png" width="40">](https://github.com/xenvre) | [@xenvre](https://github.com/xenvre) |
