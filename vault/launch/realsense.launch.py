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
            os.path.join(get_package_share_directory("vault"),
                         "launch", "rs.launch.py")
        ),
        launch_arguments={
            "node_namespace": [namespace, "/camera"],
            "node_name": "camera",
            "camera_name": [namespace, "/camera"],
            "device_type": "d435",
            # "enable_gyro": "true",
            # "enable_accel": "true",
            # "unite_imu_method": "1",
            "pointcloud.enable": "true",
            "align_depth.enable": "true",
            # "enable_infra1": "true",
            # "enable_infra2": "true"}.items()
    )

    ld = LaunchDescription()
    ld.add_action(namespace_cmd)
    ld.add_action(realsense_cmd)

    return ld
