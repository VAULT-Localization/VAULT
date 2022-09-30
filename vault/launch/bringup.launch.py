import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument


def generate_launch_description():

    ### ARGS ###
    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace",
        default_value="vault",
        description="Vault namespace")

    ### LAUNCHS ###
    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_description"),
                         "launch", "robot_state_publisher.launch.py")
        )
    )

    ## Sensors ##
    t265_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_sensors"),
                         "launch", "t265.launch.py")
        ),
        launch_arguments={
            "namespace": namespace
        }.items()
    )

    d435i_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_sensors"),
                         "launch", "d435i.launch.py")
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

    imu_hfi_a9_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_sensors"),
                         "launch", "imu_hfi_a9.launch.py")
        ),
        launch_arguments={
            "namespace": namespace
        }.items()
    )

    ## Localization ##
    localization_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_localization"),
                         "launch", "localization.launch.py")
        ),
        launch_arguments={
            "namespace": namespace,
            "use_sim_time": "False",

            "fix_t265_odom": os.getenv("FIX_T265_ODOM", default="True"),
            "publish_t265_odom_tf": os.getenv("PUBLISH_T265_ODOM_TF", default="False"),
            "fix_d435i_imu": os.getenv("FIX_D435i_IMU", default="False"),

            "publish_visual_slam_tf": os.getenv("PUBLISH_VISUAL_SLAM_TF", default="True"),
            "use_t265": os.getenv("USE_T265", default="False"),
            "use_gps": os.getenv("USE_GPS", default="True").lower(),

            "run_ekf": os.getenv("RUN_EKF", default="False"),
            "run_dual_ekf": os.getenv("RUN_DUAL_EKF", default="False"),

            "run_rgbd_odometry": os.getenv("RUN_RDGD_ODOMETRY", default="False"),
            "run_stereo_odometry": os.getenv("RUN_STEREO_ODOMETRY", default="False"),
            "run_icp_odometry": os.getenv("RUN_ICP_ODOMETRY", default="False"),
        }.items()
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(t265_cmd)
    ld.add_action(d435i_cmd)
    ld.add_action(ubx_cmd)
    ld.add_action(imu_hfi_a9_cmd)
    ld.add_action(localization_cmd)

    return ld
