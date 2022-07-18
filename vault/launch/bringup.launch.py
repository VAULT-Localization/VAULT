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

    use_camera_imu = LaunchConfiguration("use_camera_imu")
    use_camera_imu_cmd = DeclareLaunchArgument(
        "use_camera_imu",
        default_value="True",
        description="Whether to use camera IMU")

    use_visual_slam = LaunchConfiguration("use_visual_slam")
    use_visual_slam_cmd = DeclareLaunchArgument(
        "use_visual_slam",
        default_value="True",
        description="Wheter to use visual SLAM or EKF map")

    localization_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_localization"),
                         "launch", "localization.launch.py")
        ),
        launch_arguments={"namespace": namespace,
                          "use_sim_time": "False",
                          "use_visual_slam": use_visual_slam
                          }.items()
    )

    realsense_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_sensors"),
                         "launch", "realsense.launch.py")
        ),
        launch_arguments={
            "namespace": namespace,
            "use_camera_imu": use_camera_imu
        }.items()
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_description"),
                         "launch", "robot_state_publisher.launch.py")
        ),
        launch_arguments={
            "namespace": namespace
        }.items()
    )

    ubx_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_sensors"),
                         "launch", "ubx.launch.py")
        ),
        launch_arguments={
            "namespace": namespace
        }.items()
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(use_camera_imu_cmd)
    ld.add_action(use_visual_slam_cmd)

    ld.add_action(realsense_cmd)
    ld.add_action(localization_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(ubx_cmd)

    return ld
