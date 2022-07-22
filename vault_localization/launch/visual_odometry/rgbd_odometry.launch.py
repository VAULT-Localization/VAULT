from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace",
        default_value="vault",
        description="Vault namespace")

    parameters = [{
        "frame_id": "base_link",
        "odom_frame_id": "odom",
        "subscribe_depth": True,
        "subscribe_rgb": True,
        "subscribe_rgbd": False,
        "approx_sync": False,
        "publish_tf": False,
        "wait_imu_to_init": False,
        "publish_null_when_lost": False,
        "qos": 2,
        "qos_camera_info": 2,

        # 0=TORO, 1=g2o, 2=GTSAM and 3=Ceres
        "Optimizer/Strategy": "2",
        "Optimizer/GravitySigma": "0.3",

        # 0=Frame-to-Map (F2M) 1=Frame-to-Frame (F2F) 2=Fovis 3=viso2 4=DVO-SLAM 5=ORB_SLAM2 6=OKVIS 7=LOAM 8=MSCKF_VIO 9=VINS-Fusion 10=OpenVINS 11=FLOAM 12=Open3D
        "Odom/Strategy": "0",
        "Odom/ResetCountdown": "1",
        "Odom/Holonomic": "true",
        # 0=No filtering 1=Kalman filtering 2=Particle filtering
        "Odom/FilteringStrategy": "1",
        "Odom/ParticleSize": "500",
        "Odom/GuessMotion": "true",
        "Odom/AlignWithGround": "false",

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
        # subs
        ("rgb/image", "d435i/color/image_raw"),
        ("rgb/camera_info", "d435i/color/camera_info"),
        ("depth/image", "d435i/aligned_depth_to_color/image_raw"),
        ("imu", "imu"),

        # pubs
        ("odom", "rgbd/odom"),
        ("odom_info", "rgbd/odom_info"),
        ("odom_info_lite", "rgbd/odom_info_lite"),
        ("odom_last_frame", "rgbd/odom_last_frame"),
        ("odom_local_map", "rgbd/odom_local_map"),
        ("odom_local_scan_map", "rgbd/odom_local_scan_map"),
        ("odom_rgbd_image", "rgbd/odom_rgbd_image")
    ]

    return LaunchDescription([
        namespace_cmd,

        Node(
            package="rtabmap_ros",
            executable="rgbd_odometry",
            output="log",
            namespace=namespace,
            parameters=parameters,
            remappings=remappings,
            arguments=["--ros-args", "--log-level", "Warn"]),
    ])
