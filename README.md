# VAULT (Visual and Autonomous Localization Kit)

<p align="center">
  <img src="./docs/logo.png" width="50%" />
</p>

VAULT is a ROS 2 kit for outdoor localization. It fuses Visual SLAM (Intel RealSense T265), GNSS/RTK (u-blox), IMU, and visual odometry (Intel RealSense D435i) through an EKF to provide a robust pose estimate.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Using a Linux service](#using-a-linux-service)

## Prerequisites

**Hardware**

- Intel RealSense T265 (tracking camera, end-of-life)
- Intel RealSense D435i (visual odometry)
- u-blox GNSS receiver, such as the u-blox ZED-F9P (RTK)
- HFI-A9 IMU

**Software**

- Ubuntu 22.04
- [ROS 2 Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html), desktop install recommended
- Build tools and librealsense dependencies:

```shell
sudo apt update
sudo apt install -y git cmake build-essential pkg-config python3-pip \
  libssl-dev libusb-1.0-0-dev libudev-dev \
  libgtk-3-dev libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev
```

Source ROS 2 in every new terminal:

```shell
source /opt/ros/humble/setup.bash
```

Optionally, install [Foxglove](https://foxglove.dev/download) to visualize the output.

## Installation

1. Create the workspace:

```shell
mkdir -p ~/ros2_ws/src
```

2. Install [librealsense](https://github.com/IntelRealSense/librealsense) [v2.50.0](https://github.com/IntelRealSense/librealsense/releases/tag/v2.50.0), which is the last version that supports the T265 camera. The default branch of the fork below is pinned to v2.50.0:

```shell
cd ~
git clone https://github.com/VAULT-Localization/librealsense.git
cd librealsense
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
sudo make install
sudo ldconfig
```

3. Install the udev rules so the cameras can be accessed without root:

```shell
sudo cp ~/librealsense/config/99-realsense-libusb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

4. Install the compatible [realsense-ros](https://github.com/IntelRealSense/realsense-ros), version [3.2.3](https://github.com/IntelRealSense/realsense-ros/releases/tag/3.2.3). The default branch of the fork below is pinned to 3.2.3:

```shell
cd ~/ros2_ws/src
git clone https://github.com/VAULT-Localization/realsense-ros.git
cd ~/ros2_ws
rosdep install --from-paths src -r -y
colcon build --symlink-install
```

5. Clone and compile VAULT and its dependencies:

```shell
cd ~/ros2_ws/src
git clone https://github.com/VAULT-Localization/VAULT.git
git clone https://github.com/VAULT-Localization/ubx_ros.git
pip3 install -r VAULT/requirements.txt
cd ~/ros2_ws
rosdep update
rosdep install --from-paths src -r -y
colcon build --symlink-install
source install/setup.bash
```

6. Verify the installation:

```shell
rs-enumerate-devices    # lists the connected RealSense cameras
ros2 pkg list | grep vault
```

### Assigning ttyUSB

Serial devices can get different names on every boot. Assign a stable symlink to each one by matching its serial number.

1. Get the serial number of each device:

```shell
sudo udevadm info --query=property --name=/dev/ttyUSB0 | grep SERIAL
# ID_SERIAL=Silicon_Labs_HandsFree_IMU_USB_to_UART_Bridge_Controller_0001
# ID_SERIAL_SHORT=0001

sudo udevadm info --query=property --name=/dev/ttyACM0 | grep SERIAL
# ID_SERIAL=u-bloxAG-_www.u-blox.com_u-blox_GNSS_receiver
```

2. Create the udev rules file:

```shell
sudo nano /etc/udev/rules.d/99-usbserial.rules
```

Add the following lines, replacing the `ID_SERIAL` values with the ones from your devices:

```
ACTION=="add",ENV{ID_BUS}=="usb",ENV{ID_SERIAL}=="Silicon_Labs_HandsFree_IMU_USB_to_UART_Bridge_Controller_0001",SYMLINK+="ttyUSB0"
ACTION=="add",ENV{ID_BUS}=="usb",ENV{ID_SERIAL}=="u-bloxAG-_www.u-blox.com_u-blox_GNSS_receiver",SYMLINK+="ttyACM0"
```

3. Reload the udev rules:

```shell
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Usage

Define the following environment variables. They select which sensors and estimators are launched; anything disabled is skipped:

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

Launch VAULT:

```shell
ros2 launch vault_bringup vault.launch.py
```

### Using a Linux service

[See vault_service README.](./vault_service/README.md)

<!-- ## Docs

### Frames

![](./docs/frames.png)

### Rosgraph

![](./docs/rosgraph.png) -->
