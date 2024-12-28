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
        "namespace", default_value="vault", description="Vault namespace"
    )

    realsense_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("vault_sensors"), "launch", "rs.launch.py"
            )
        ),
        launch_arguments={
            "node_namespace": [namespace, "/d435i"],
            "node_name": "d435i",
            "camera_name": [namespace, "_d435i"],
            "device_type": "d435",
            "enable_gyro": "true",
            "enable_accel": "true",
            "unite_imu_method": "2",
            "pointcloud.enable": "false",
            "align_depth.enable": "true",
            "enable_sync": "true",
            "linear_accel_cov": "1.0",
            "decimation_filter.enable": "true",
            "disparity_filter.enable": "true",
            "hole_filling_filter.enable": "true",
            "spatial_filter.enable": "true",
            "temporal_filter.enable": "true",
            "enable_infra1": "false",
            "enable_infra2": "false",
        }.items(),
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(realsense_cmd)

    return ld
