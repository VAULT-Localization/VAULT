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

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time",
        default_value="False",
        description="Use simulation (Gazebo) clock if True")

    rgbd_odometry_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_dir,
                         "launch/localization", "rgbd_odometry.launch.py")
        ),
        launch_arguments={"namespace": namespace}.items()
    )

    rtabmap_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_dir,
                         "launch/localization", "rtabmap.launch.py")
        ),
        launch_arguments={
            "namespace": namespace,
            "use_sim_time": use_sim_time
        }.items()
    )

    ekf_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_dir,
                         "launch/localization", "ekf.launch.py")
        ),
        launch_arguments={"namespace": namespace,
                          "use_sim_time": use_sim_time
                          }.items()
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(use_sim_time_cmd)

    ld.add_action(rgbd_odometry_cmd)
    ld.add_action(rtabmap_cmd)
    ld.add_action(ekf_cmd)

    return ld
