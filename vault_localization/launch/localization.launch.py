import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch_ros.actions import Node


def generate_launch_description():

    vault_localization_dir = get_package_share_directory("vault_localization")

    ### ARGS ###
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

    ## Sensors ##
    fix_t265_odom = LaunchConfiguration("fix_t265_odom")
    fix_t265_odom_cmd = DeclareLaunchArgument(
        "fix_t265_odom",
        default_value="True",
        description="Wheter to fix odom of T265")

    publish_t265_odom_tf = LaunchConfiguration("publish_t265_odom_tf")
    publish_t265_odom_tf_cmd = DeclareLaunchArgument(
        "publish_t265_odom_tf",
        default_value="True",
        description="Wheter to publish odom tf of T265")

    fix_d435i_imu_filter = LaunchConfiguration("fix_d435i_imu_filter")
    fix_d435i_imu_filter_cmd = DeclareLaunchArgument(
        "fix_d435i_imu_filter",
        default_value="True",
        description="Wheter to fix D435i imu data")

    ## VSLAM ##
    publish_visual_slam_tf = LaunchConfiguration("publish_visual_slam_tf")
    publish_visual_slam_tf_cmd = DeclareLaunchArgument(
        "publish_visual_slam_tf",
        default_value="True",
        description="Wheter to publish visual SLAM tf map or EKF one")

    use_t265 = LaunchConfiguration("use_t265")
    use_t265_cmd = DeclareLaunchArgument(
        "use_t265",
        default_value="False",
        description="Wheter to use T265 camera or D435i for visual SLAM")

    use_gps = LaunchConfiguration("use_gps")
    use_gps_cmd = DeclareLaunchArgument(
        "use_gps",
        default_value="True",
        description="Wheter to use GPS data in the loop clousure")

    ## EKF ##
    run_ekf = LaunchConfiguration("run_ekf")
    run_ekf_cmd = DeclareLaunchArgument(
        "run_ekf",
        default_value="False",
        description="Wheter to run EKF")

    run_dual_ekf = LaunchConfiguration("run_dual_ekf")
    run_dual_ekf_cmd = DeclareLaunchArgument(
        "run_dual_ekf",
        default_value="False",
        description="Wheter to run dual EKF (GPS+IMU+Odom)")

    ## Visual Odometry ##
    run_rgbd_odometry = LaunchConfiguration("run_rgbd_odometry")
    run_rgbd_odometry_cmd = DeclareLaunchArgument(
        "run_rgbd_odometry",
        default_value="False",
        description="Wheter to run rgd odometry")

    run_stereo_odometry = LaunchConfiguration("run_stereo_odometry")
    run_stereo_odometry_cmd = DeclareLaunchArgument(
        "run_stereo_odometry",
        default_value="False",
        description="Wheter to run stereo odometry")

    run_icp_odometry = LaunchConfiguration("run_icp_odometry")
    run_icp_odometry_cmd = DeclareLaunchArgument(
        "run_icp_odometry",
        default_value="False",
        description="Wheter to run icp odometry")

    ### LAUNCHS & NODES ###

    ## Sensors ##
    fix_odom_frame_cmd = Node(
        package="vault_sensors",
        executable="fix_odom_frame_node",
        name="fix_odom_frame_node",
        namespace=namespace,
        output="screen",
        parameters=[{"frame_id": "base_link",
                     "odom_frame": "odom",
                     "publish_tf": publish_t265_odom_tf}],
        remappings=[("odom_out", "t265/odom"),
                    ("odom_in", "t265/pose/sample")],
        condition=IfCondition(PythonExpression([fix_t265_odom]))
    )

    imu_filter_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("vault_sensors"),
                         "launch", "imu_filter.launch.py")
        ),
        launch_arguments={
            "namespace": namespace
        }.items(),
        condition=IfCondition(PythonExpression([fix_d435i_imu_filter]))
    )

    ## VSLAM ##
    rtabmap_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch/visual_slam", "rtabmap.launch.py")
        ),
        launch_arguments={
            "namespace": namespace,
            "use_sim_time": use_sim_time,
            "publish_visual_slam_tf": publish_visual_slam_tf,
            "use_t265": use_t265,
            "use_gps": use_gps
        }.items()
    )

    ## EKF ##
    ekf_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch/ekf", "ekf.launch.py")
        ),
        launch_arguments={"namespace": namespace,
                          "use_sim_time": use_sim_time
                          }.items(),
        condition=IfCondition(PythonExpression([run_ekf]))
    )

    dual_ekf_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch/ekf", "dual_ekf.launch.py")
        ),
        launch_arguments={"namespace": namespace,
                          "use_sim_time": use_sim_time
                          }.items(),
        condition=IfCondition(PythonExpression([run_dual_ekf]))
    )

    ## Visual Odometry ##
    rgbd_odometry_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch/visual_odometry", "rgbd_odometry.launch.py")
        ),
        launch_arguments={"namespace": namespace}.items(),
        condition=IfCondition(PythonExpression([run_rgbd_odometry]))
    )

    stereo_odometry_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch/visual_odometry", "stereo_odometry.launch.py")
        ),
        launch_arguments={"namespace": namespace}.items(),
        condition=IfCondition(PythonExpression([run_stereo_odometry]))
    )

    icp_odometry_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vault_localization_dir,
                         "launch/visual_odometry", "icp_odometry.launch.py")
        ),
        launch_arguments={"namespace": namespace}.items(),
        condition=IfCondition(PythonExpression([run_icp_odometry]))
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(use_sim_time_cmd)

    ## Sensors ##
    ld.add_action(fix_t265_odom_cmd)
    ld.add_action(publish_t265_odom_tf_cmd)
    ld.add_action(fix_d435i_imu_filter_cmd)

    ld.add_action(fix_odom_frame_cmd)
    ld.add_action(imu_filter_cmd)

    ## VSLAM ##
    ld.add_action(publish_visual_slam_tf_cmd)
    ld.add_action(use_t265_cmd)
    ld.add_action(use_gps_cmd)

    ld.add_action(rtabmap_cmd)

    ## EKF ##
    ld.add_action(run_ekf_cmd)
    ld.add_action(run_dual_ekf_cmd)

    ld.add_action(ekf_cmd)
    ld.add_action(dual_ekf_cmd)

    ## Visual Odometry ##
    ld.add_action(run_rgbd_odometry_cmd)
    ld.add_action(run_stereo_odometry_cmd)
    ld.add_action(run_icp_odometry_cmd)

    ld.add_action(rgbd_odometry_cmd)
    ld.add_action(stereo_odometry_cmd)
    ld.add_action(icp_odometry_cmd)

    return ld
