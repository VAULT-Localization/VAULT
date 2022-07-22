import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition


def generate_launch_description():

    vault_localization_dir = get_package_share_directory("vault_localization")

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

    use_visual_slam = LaunchConfiguration("use_visual_slam")
    use_visual_slam_cmd = DeclareLaunchArgument(
        "use_visual_slam",
        default_value="True",
        description="Wheter to use visual SLAM or EKF map")

    use_t265 = LaunchConfiguration("use_t265")
    use_t265_cmd = DeclareLaunchArgument(
        "use_t265",
        default_value="False",
        description="Wheter to use T265 camera or D435i for visual SLAM")

    rgbd_odometry_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch/visual_odometry", "rgbd_odometry.launch.py")
        ),
        launch_arguments={"namespace": namespace}.items()
    )

    rtabmap_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch/visual_slam", "rtabmap.launch.py")
        ),
        launch_arguments={
            "namespace": namespace,
            "use_sim_time": use_sim_time,
            "use_t265": use_t265
        }.items(),
        condition=IfCondition(PythonExpression([use_visual_slam]))
    )

    ekf_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch/ekf", "dual_ekf.launch.py")
        ),
        launch_arguments={"namespace": namespace,
                          "use_sim_time": use_sim_time
                          }.items()
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(use_sim_time_cmd)
    ld.add_action(use_visual_slam_cmd)
    ld.add_action(use_t265_cmd)

    # ld.add_action(rgbd_odometry_cmd)
    ld.add_action(rtabmap_cmd)
    # ld.add_action(ekf_cmd)

    return ld
