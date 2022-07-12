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
                remappings=[("imu/data_raw", "camera/imu"),
                            ("imu/data", "imu")]
            )
        ]
    )
