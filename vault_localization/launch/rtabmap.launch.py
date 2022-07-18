import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.conditions import IfCondition
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression


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
        "frame_id": "base_link",
        "map_frame_id": "map",
        "subscribe_depth": True,
        "subscribe_rgb": True,
        "subscribe_scan": False,
        "subscribe_odom": True,
        "subscribe_odom_info": False,
        "odom_sensor_sync": True,
        "approx_sync": True,
        "publish_tf": True,
        "use_sim_time": use_sim_time,
        "qos_image": 2,
        "qos_camera_info": 2,
        "qos_gps": 2,
        "qos_imu": 2,
        "qos_scan": 2,
        "queue_size": 30,

        "Rtabmap/LoopGPS": "true",

        # 0=TORO, 1=g2o, 2=GTSAM and 3=Ceres
        "Optimizer/Strategy": "2",
        "Optimizer/GravitySigma": "0.3",

        "RGBD/OptimizeMaxError": "1.0",
        "RGBD/OptimizeFromGraphEnd": "true",
        "RGBD/LocalRadius": "20",

        "Grid/DepthDecimation": "2",
        # "Grid/RangeMin": "0.0",
        # "Grid/RangeMax": "3.0",
        "Grid/MinClusterSize": "20",
        "Grid/MaxGroundAngle": "35",
        "Grid/NormalK": "20",
        "Grid/CellSize": "0.1",
        "Grid/FlatObstacleDetected": "false",

        "GridGlobal/UpdateError": "0.01",
        "GridGlobal/MinSize": "200",

        "GFTT/MinDistance": "2",
        "GFTT/QualityLevel": "0.1",
        "GFTT/BlockSize": "4",
        "GFTT/UseHarrisDetector": "false",
        "GFTT/K": "0.04",

        "SURF/Extended": "true",
        "SURF/HessianThreshold": "500",
        "SURF/Octaves": "4",
        "SURF/OctaveLayers": "4",
        "SURF/Upright": "false",
        "SURF/GpuVersion": "false",
        "SURF/GpuKeypointsRatio": "0.01",

        "SIFT/NFeatures": "1000",
        "SIFT/NOctaveLayers": "4",
        "SIFT/RootSIFT": "false",

        "FREAK/OrientationNormalized": "true",
        "FREAK/ScaleNormalized": "true",
        "FREAK/PatternScale": "30",
        "FREAK/NOctaves": "4",

        "KAZE/Extended": "true",
        "KAZE/Upright": "false",
        "KAZE/NOctaves": "4",
        "KAZE/NOctaveLayers": "4",
        # 0=DIFF_PM_G1, 1=DIFF_PM_G2, 2=DIFF_WEICKERT or 3=DIFF_CHARBONNIER
        "KAZE/Diffusivity": "1",

        "BRIEF/Bytes": "128",

        # 0=SURF 1=SIFT 2=ORB 3=FAST/FREAK 4=FAST/BRIEF 5=GFTT/FREAK 6=GFTT/BRIEF 7=BRISK 8=GFTT/ORB 9=KAZE 10=ORB-OCTREE 11=SuperPoint 12=SURF/FREAK 13=GFTT/DAISY 14=SURF/DAISY 15=PyDetector
        "Vis/FeatureType": "8",
        "Vis/DepthAsMask": "true",
        "Vis/FeatureWindowSize": "9",
        "Vis/CorGuessWinSize": "40",
        "Vis/MaxFeatures": "1000",
        # 0=Features Matching, 1=Optical Flow
        "Vis/CorType": "0",
        # kNNFlannNaive=0, kNNFlannKdTree=1, kNNFlannLSH=2, kNNBruteForce=3, kNNBruteForceGPU=4, BruteForceCrossCheck=5, SuperGlue=6, GMS=7
        "Vis/CorNNType": "1"

    }]

    remappings = [
        ("rgb/image", "camera/color/image_raw"),
        ("rgb/camera_info", "camera/color/camera_info"),
        ("depth/image", "camera/aligned_depth_to_color/image_raw"),
        ("imu", "imu"),
        ("odom", "odom"),
        ("odom_info", "odom_info"),
        ("goal", "goal_pose"),
        ("gps/fix", "fix")
    ]

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

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory("vault_visualization"),
                             "launch", "rtabmapviz.launch.py")
            ),
            condition=IfCondition(PythonExpression([launch_rtabmapviz]))
        )

    ])
