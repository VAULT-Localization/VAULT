# Copyright (C) 2023 Miguel Ángel González Santamarta

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument


def generate_launch_description():

    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace",
        default_value="vault",
        description="Vault namespace",
    )

    use_camera_imu = LaunchConfiguration("use_camera_imu")
    use_camera_imu_cmd = DeclareLaunchArgument(
        "use_camera_imu",
        default_value="True",
        description="Whether to use camera IMU",
    )

    realsense_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("vault_sensors"), "launch", "rs.launch.py"
            )
        ),
        launch_arguments={
            "node_namespace": [namespace, "/t265"],
            "node_name": "t265_node",
            "camera_name": [namespace, "_t265"],
            "device_type": "t265",
            "enable_gyro": use_camera_imu,
            "enable_accel": use_camera_imu,
            "enable_pose": "true",
            "unite_imu_method": "2",
            "align_depth.enable": "false",
            "enable_sync": "true",
            "linear_accel_cov": "1.0",
            "publish_odom_tf": "false",
            "enable_fisheye1": "false",
            "enable_fisheye2": "false",
            "publish_tf": "false",
        }.items(),
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(use_camera_imu_cmd)

    ld.add_action(realsense_cmd)

    return ld
