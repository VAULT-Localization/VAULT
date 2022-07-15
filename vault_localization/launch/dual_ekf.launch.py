import os
from launch import LaunchDescription
import launch_ros.actions
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from nav2_common.launch import RewrittenYaml


def generate_launch_description():

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

    params_file = os.path.join(get_package_share_directory(
        "vault_localization"), "config", "dual_ekf.yaml")

    param_substitutions = {
        "use_sim_time": use_sim_time}

    configured_params = RewrittenYaml(
        source_file=params_file,
        param_rewrites=param_substitutions,
        convert_types=True)

    return LaunchDescription([
        namespace_cmd,
        use_sim_time_cmd,

        launch_ros.actions.Node(
            package="robot_localization",
            executable="ekf_node",
            name="ekf_filter_node_odom",
            namespace=namespace,
            output="screen",
            parameters=[configured_params],
            remappings=[("odometry/filtered", "odom_local")]
        ),

        launch_ros.actions.Node(
            package="robot_localization",
            executable="ekf_node",
            name="ekf_filter_node_map",
            namespace=namespace,
            output="screen",
            parameters=[configured_params],
            remappings=[("odometry/filtered", "odom_global")]
        ),

        launch_ros.actions.Node(
            package="robot_localization",
            executable="navsat_transform_node",
            name="navsat_transform",
            namespace=namespace,
            output="screen",
            parameters=[configured_params],
            remappings=[("imu/data", "imu"),
                        ("gps/fix", "fix"),
                        ("gps/filtered", "gps"),
                        ("odometry/gps", "odom_gps"),
                        ("odometry/filtered", "odom_global")]

        )
    ])
