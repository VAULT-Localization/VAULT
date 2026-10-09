#!/bin/bash
source /opt/ros/${ROS_DISTRO:-humble}/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch vault_bringup vault.launch.py
