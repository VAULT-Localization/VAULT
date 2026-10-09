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
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.actions import DeclareLaunchArgument


def generate_launch_description():

    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace", default_value="vault", description="Vault namespace"
    )

    enable_imu = LaunchConfiguration("enable_imu")
    enable_imu_cmd = DeclareLaunchArgument(
        "enable_imu",
        default_value="False",
        description="Whether to enable D435i gyro and accel streams",
    )

    enable_infra = LaunchConfiguration("enable_infra")
    enable_infra_cmd = DeclareLaunchArgument(
        "enable_infra",
        default_value="False",
        description="Whether to enable D435i infra streams",
    )

    enable_pointcloud = LaunchConfiguration("enable_pointcloud")
    enable_pointcloud_cmd = DeclareLaunchArgument(
        "enable_pointcloud",
        default_value="False",
        description="Whether to enable D435i pointcloud",
    )

    realsense_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("vault_sensors"), "launch", "rs.launch.py"
            )
        ),
        launch_arguments={
            "node_namespace": [namespace, "/d435i"],
            "node_name": "d435i_node",
            "camera_name": [namespace, "_d435i"],
            "device_type": "d435",
            "enable_gyro": enable_imu,
            "enable_accel": enable_imu,
            "unite_imu_method": PythonExpression(
                ["'2' if '", enable_imu, "'.lower() == 'true' else '0'"]
            ),
            "pointcloud.enable": enable_pointcloud,
            "align_depth.enable": "true",
            "enable_sync": "true",
            "linear_accel_cov": "1.0",
            "decimation_filter.enable": "true",
            "enable_infra1": enable_infra,
            "enable_infra2": enable_infra,
            "publish_tf": "false",
        }.items(),
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(enable_imu_cmd)
    ld.add_action(enable_infra_cmd)
    ld.add_action(enable_pointcloud_cmd)

    ld.add_action(realsense_cmd)

    return ld
