# VAULT (Visual and Autonomous Localization Kit)

<p align="center">
  <img src="./docs/logo.png" width="50%" />
</p>

## Table of Contents

1. [Installation](#installation)
2. [Docs](#docs)

## Installation

```shell
$ cd ~/ros2_ws/src
$ git clone https://github.com/mgonzs13/VAULT.git
$ git clone https://github.com/mgonzs13/ubx_ros
$ pip3 install -r VAULT/requirements.txt
$ cd ~/ros2_ws
$ rosdep install --from-paths src -r -y
$ colcon build
```

### Others
- [librealsense](https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md)
- [Foxglove](https://foxglove.dev/download)


## Usage

### Running VAULT

Define the following environment variables:

```shell
# Ntrip
export NTRIP_HOST=YOUR_HOST
export NTRIP_PORT=YOUR_PORT
export NTRIP_MOUNTPOINT=YOUR_POINT
export NTRIP_USER=YOUR_USER
export NTRIP_PASSWORD=YOUR_PASSWORD

# ROS 2
export ROS_DOMAIN_ID=13
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

# Sensors
export FIX_T265_ODOM=True
export PUBLISH_T265_ODOM_TF=False
export FIX_D435i_IMU=False

# Visual SLAM
export PUBLISH_VISUAL_SLAM_TF=True
export USE_T265=False
export USE_GPS=False

# EKF
export RUN_EKF=True
export RUN_DUAL_EKF=False

# Visual odometry
export RUN_RDGD_ODOMETRY=False
export RUN_STEREO_ODOMETRY=False
export RUN_ICP_ODOMETRY=False
```

```shell
$ ros2 launch vault_bringup vault.launch.py
```

### Using a Linux service

[See vault_service README.](./vault_service/README.md)


<!-- ## Docs

### Frames

![](./docs/frames.png)

### Rosgraph

![](./docs/rosgraph.png) -->
