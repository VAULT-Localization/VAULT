from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument


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

    parameters = [{
        "frame_id": "vault_base_link",
        "odom_frame_id": "vault_odom",
        "map_frame_id": "vault_map",
        "subscribe_depth": True,
        "subscribe_rgb": True,
        "subscribe_scan": False,
        "subscribe_odom_info": True,
        "approx_sync": True,
        "publish_tf": True,
        "use_sim_time": use_sim_time,
        "qos_image": 2,
        "qos_camera_info": 2,
        "qos_gps": 2,
        "qos_imu": 2,
        "qos_scan": 2,
    }]

    remappings = [
        ("rgb/image", "camera/color/image_raw"),
        ("rgb/camera_info", "camera/color/camera_info"),
        ("depth/image", "camera/aligned_depth_to_color/image_raw"),
        ("imu", "imu"),
        ("odom", "odom"),
        ("odom_info", "odom_info"),
        ("goal", "goal_pose"),
        ("gps/fix", "fix")]

    return LaunchDescription([
        namespace_cmd,
        use_sim_time_cmd,

        Node(
            package="rtabmap_ros",
            executable="rtabmapviz",
            output="screen",
            namespace=namespace,
            parameters=parameters,
            remappings=remappings),
    ])
