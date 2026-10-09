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
from launch import LaunchDescription
import launch_ros.actions
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from nav2_common.launch import RewrittenYaml


def generate_launch_description():

    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace", default_value="vault", description="Vault namespace"
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time",
        default_value="False",
        description="Use simulation (Gazebo) clock if True",
    )

    ekf_odom_params_file = os.path.join(
        get_package_share_directory("vault_localization"),
        "config/dual_ekf",
        "ekf_odom.yaml",
    )
    ekf_map_params_file = os.path.join(
        get_package_share_directory("vault_localization"),
        "config/dual_ekf",
        "ekf_map.yaml",
    )
    navsat_transform_params_file = os.path.join(
        get_package_share_directory("vault_localization"),
        "config/dual_ekf",
        "navsat_transform.yaml",
    )

    param_substitutions = {"use_sim_time": use_sim_time}

    ekf_odom_params = RewrittenYaml(
        source_file=ekf_odom_params_file,
        param_rewrites=param_substitutions,
        convert_types=True,
    )

    ekf_map_params = RewrittenYaml(
        source_file=ekf_map_params_file,
        param_rewrites=param_substitutions,
        convert_types=True,
    )

    navsat_transform_params = RewrittenYaml(
        source_file=navsat_transform_params_file,
        param_rewrites=param_substitutions,
        convert_types=True,
    )

    return LaunchDescription(
        [
            namespace_cmd,
            use_sim_time_cmd,
            launch_ros.actions.Node(
                package="robot_localization",
                executable="ekf_node",
                name="ekf_filter_node_odom",
                namespace=namespace,
                output="screen",
                parameters=[ekf_odom_params],
                remappings=[
                    # pubs
                    ("odometry/filtered", "odom")
                ],
            ),
            launch_ros.actions.Node(
                package="robot_localization",
                executable="ekf_node",
                name="ekf_filter_node_map",
                namespace=namespace,
                output="screen",
                parameters=[ekf_map_params],
                remappings=[
                    # pubs
                    ("odometry/filtered", "odom_global")
                ],
            ),
            launch_ros.actions.Node(
                package="robot_localization",
                executable="navsat_transform_node",
                name="navsat_transform",
                namespace=namespace,
                output="screen",
                parameters=[navsat_transform_params],
                remappings=[
                    # subs
                    ("gps/fix", "gps/fix"),
                    ("imu", "imu"),
                    ("odometry/filtered", "odom_global"),
                    # pubs
                    ("gps/filtered", "gps/fix_filtered"),
                    ("odometry/gps", "gps/odom"),
                ],
            ),
        ]
    )
