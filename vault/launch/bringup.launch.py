import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition


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

    localization_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_localization"),
                         "launch", "localization.launch.py")
        ),
        launch_arguments={"namespace": namespace,
                          "use_sim_time": "False"
                          }.items()
    )

    realsense_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_sensors"),
                         "launch", "realsense.launch.py")
        ),
        launch_arguments={
            "namespace": namespace
        }.items()
    )

    imu_filter_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_sensors"),
                         "launch", "imu_filter.launch.py")
        ),
        launch_arguments={
            "namespace": namespace
        }.items(),
        condition=IfCondition(PythonExpression([use_camera_imu]))
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

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(use_camera_imu_cmd)

    ld.add_action(realsense_cmd)
    ld.add_action(imu_filter_cmd)
    ld.add_action(localization_cmd)
    ld.add_action(robot_state_publisher_cmd)

    return ld
