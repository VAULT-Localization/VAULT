import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node


def generate_launch_description():

    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace",
        default_value="vault",
        description="Vault namespace")

    use_camera_imu = LaunchConfiguration("use_camera_imu")
    use_camera_imu_cmd = DeclareLaunchArgument(
        "use_camera_imu",
        default_value="True",
        description="Whether to use camera IMU")

    realsense_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_sensors"),
                         "launch", "rs.launch.py")
        ),
        launch_arguments={
            "node_namespace": [namespace, "/camera"],
            "node_name": "camera",
            "camera_name": [namespace, "_camera"],
            "device_type": "t265",
            "enable_gyro": use_camera_imu,
            "enable_accel": use_camera_imu,
            "enable_pose": "true",
            "unite_imu_method": "2",
            "align_depth.enable": "false",
            "enable_sync": "true",
            "linear_accel_cov": "1.0",
            "publish_odom_tf": "false",
        }.items()
    )

    fix_odom_frame_cmd = Node(
        package="vault_sensors",
        executable="fix_odom_frame_node",
        name="fix_odom_frame_node",
        namespace=LaunchConfiguration("namespace"),
        output="screen",
        parameters=[{"frame_id": "base_link",
                     "odom_frame": "odom"}],
        remappings=[("odom_out", "odom"),
                    ("odom_in", "camera/pose/sample")]
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(use_camera_imu_cmd)

    ld.add_action(realsense_cmd)
    ld.add_action(fix_odom_frame_cmd)

    return ld
