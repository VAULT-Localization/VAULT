# Copyright (C) 2023  Miguel Ángel González Santamarta

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
import launch
import launch.actions
import launch.substitutions
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument


def generate_launch_description():

    config_dir = os.path.join(get_package_share_directory(
        "vault_sensors"), "config")

    return launch.LaunchDescription(
        [

            DeclareLaunchArgument(
                "namespace",
                default_value="vault",
                description="Vault namespace"),

            launch_ros.actions.Node(
                package="imu_filter_madgwick",
                executable="imu_filter_madgwick_node",
                name="imu_filter",
                namespace=LaunchConfiguration("namespace"),
                output="screen",
                parameters=[os.path.join(config_dir, "imu_filter.yaml")],
                remappings=[("imu/data_raw", "d435i/imu"),
                            ("imu/data", "d435i/imu/data")]
            ),

            launch_ros.actions.Node(
                package="vault_sensors",
                executable="fix_imu_frame_node",
                name="fix_imu_frame_node",
                namespace=LaunchConfiguration("namespace"),
                output="screen",
                parameters=[{"new_frame": "imu_optical_frame",
                             "frame_prefix": [LaunchConfiguration("namespace"), "_d435i"]}],
                remappings=[("imu/data", "d435i/imu/data"),
                            ("imu", "d435i/imu/fix_data")]
            )
        ]
    )
