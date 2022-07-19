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

    use_rgbd_odom = LaunchConfiguration("use_rgbd_odom")
    use_rgbd_odom_cmd = DeclareLaunchArgument(
        "use_rgbd_odom",
        default_value="True",
        description="Wheter to use visual RGBD odometry")

    rgbd_odometry_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch", "rgbd_odometry.launch.py")
        ),
        launch_arguments={"namespace": namespace}.items(),
        condition=IfCondition(PythonExpression([use_rgbd_odom]))
    )

    rtabmap_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch", "rtabmap.launch.py")
        ),
        launch_arguments={
            "namespace": namespace,
            "use_sim_time": use_sim_time,
            "use_rgbd": use_rgbd_odom
        }.items(),
        condition=IfCondition(PythonExpression([use_visual_slam]))
    )

    ekf_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch", "ekf.launch.py")
        ),
        launch_arguments={"namespace": namespace,
                          "use_sim_time": use_sim_time
                          }.items(),
        condition=IfCondition(PythonExpression(
            [use_visual_slam, " and ", use_rgbd_odom]))
    )

    dual_ekf_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch", "dual_ekf.launch.py")
        ),
        launch_arguments={"namespace": namespace,
                          "use_sim_time": use_sim_time
                          }.items(),
        condition=UnlessCondition(PythonExpression([use_visual_slam]))
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(use_sim_time_cmd)
    ld.add_action(use_visual_slam_cmd)
    ld.add_action(use_rgbd_odom_cmd)

    ld.add_action(rgbd_odometry_cmd)
    ld.add_action(rtabmap_cmd)
    ld.add_action(ekf_cmd)
    ld.add_action(dual_ekf_cmd)

    return ld
