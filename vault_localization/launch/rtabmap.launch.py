from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition


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

    launch_rtabmapviz = LaunchConfiguration("launch_rtabmapviz")
    launch_rtabmapviz_cmd = DeclareLaunchArgument(
        "launch_rtabmapviz",
        default_value="False",
        description="Wheather to launch rtabmapviz")

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

        "Rtabmap/LoopGPS": "true",

        "Optimizer/Strategy": "1",
        "Optimizer/GravitySigma": "0.0",

        "RGBD/OptimizeMaxError": "1.0",
        "RGBD/OptimizeFromGraphEnd": "true",
        "RGBD/LocalRadius": "20",

        "GFTT/MinDistance": "2.5",
        "GFTT/QualityLevel": "0.1",

        "Vis/CorGuessWinSize": "40",
        "Vis/CorType": "0",
        "Vis/MaxFeatures": "1000",
        "Vis/MinDepth": "0.0",
        "Vis/MaxDepth": "2.5",

        "Grid/DepthDecimation": "2",
        "Grid/RangeMin": "0.0",
        "Grid/RangeMax": "2.5",
        "Grid/MinClusterSize": "20",
        "Grid/MaxGroundAngle": "35",
        "Grid/NormalK": "20",
        "Grid/CellSize": "0.1",
        "Grid/FlatObstacleDetected": "false",

        "GridGlobal/UpdateError": "0.01",
        "GridGlobal/MinSize": "200"
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
        launch_rtabmapviz_cmd,

        Node(
            package="rtabmap_ros",
            executable="rtabmap",
            output="screen",
            namespace=namespace,
            parameters=parameters,
            remappings=remappings,
            arguments=["-d",
                       "--ros-args", "--log-level", "Warn"]),

        Node(
            condition=IfCondition(launch_rtabmapviz),
            package="rtabmap_ros",
            executable="rtabmapviz",
            output="screen",
            namespace=namespace,
            parameters=parameters,
            remappings=remappings),
    ])
