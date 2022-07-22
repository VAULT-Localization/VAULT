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
        description="Vault namespace")

    realsense_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_sensors"),
                         "launch", "rs.launch.py")
        ),
        launch_arguments={
            "node_namespace": [namespace, "/d435i"],
            "node_name": "d435i",
            "camera_name": [namespace, "_d435i"],
            "device_type": "d435",
            "enable_gyro": "true",
            "enable_accel": "true",
            "unite_imu_method": "2",
            "pointcloud.enable": "true",
            "align_depth.enable": "true",
            "enable_sync": "true",
            "linear_accel_cov": "1.0",
            "decimation_filter.enable": "true",
            "disparity_filter.enable": "true",
            "hole_filling_filter.enable": "true",
            "spatial_filter.enable": "true",
            "temporal_filter.enable": "true",
            "enable_infra1": "true",
            "enable_infra2": "true"
        }.items()
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(realsense_cmd)

    return ld
