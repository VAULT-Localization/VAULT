import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument


def generate_launch_description():

    vault_dir = get_package_share_directory("vault")

    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace",
        default_value="vault",
        description="Vault namespace")

    vault_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_dir,
                         "launch", "vault.launch.py")
        ),
        launch_arguments={"namespace": namespace,
                          "use_sim_time": "False"
                          }.items()
    )

    realsense_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_dir,
                         "launch", "realsense.launch.py")
        ),
        launch_arguments={
            "namespace": namespace
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

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)

    ld.add_action(vault_cmd)
    ld.add_action(realsense_cmd)
    ld.add_action(robot_state_publisher_cmd)

    return ld
