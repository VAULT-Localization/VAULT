import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.conditions import IfCondition


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
            "pointcloud.enable": "false",
            "align_depth.enable": "true",
            "enable_sync": "true",
            "linear_accel_cov": "1.0",
            "decimation_filter.enable": "true",
            "disparity_filter.enable": "true",
            "hole_filling_filter.enable": "true",
            "spatial_filter.enable": "true",
            "temporal_filter.enable": "true",
            # "enable_infra1": "true",
            # "enable_infra2": "true"
        }.items()
    )

    imu_filter_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_sensors"),
                         "launch", "imu_filter.launch.py")
        ),
        launch_arguments={
            "namespace": namespace
        }.items()
    )

    fix_imu_frame_cmd = Node(
        package="vault_sensors",
        executable="fix_imu_frame_node",
        name="fix_imu_frame_node",
        namespace=LaunchConfiguration("namespace"),
        output="screen",
        parameters=[{"new_frame": "imu_optical_frame",
                     "frame_prefix": [namespace, "_d435i"]}],
        remappings=[("imu/data", "d435i/imu/data"),
                    ("imu", "d435i/imu/fix_data")]
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(realsense_cmd)
    ld.add_action(imu_filter_cmd)
    ld.add_action(fix_imu_frame_cmd)

    return ld
