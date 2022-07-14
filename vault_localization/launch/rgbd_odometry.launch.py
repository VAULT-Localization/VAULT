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
        "frame_id": [namespace, "_base_link"],
        "odom_frame_id": [namespace, "_odom"],
        "subscribe_depth": True,
        "subscribe_rgb": True,
        "approx_sync": True,
        "publish_tf": False,
        "wait_imu_to_init": False,
        "publish_null_when_lost": False,
        "qos": 2,
        "qos_camera_info": 2,

        # 0=TORO, 1=g2o, 2=GTSAM and 3=Ceres
        "Optimizer/Strategy": "2",
        "Optimizer/GravitySigma": "0.0",

        # 0=Frame-to-Map (F2M) 1=Frame-to-Frame (F2F) 2=Fovis 3=viso2 4=DVO-SLAM 5=ORB_SLAM2 6=OKVIS 7=LOAM 8=MSCKF_VIO 9=VINS-Fusion 10=OpenVINS 11=FLOAM 12=Open3D
        "Odom/Strategy": "1",
        "Odom/ResetCountdown": "1",
        "Odom/Holonomic": "true",
        # 0=No filtering 1=Kalman filtering 2=Particle filtering
        "Odom/FilteringStrategy": "1",
        "Odom/ParticleSize": "400",

        "GFTT/MinDistance": "7",
        "GFTT/QualityLevel": "0.001",

        "SURF/Extended": "false",
        "SURF/Upright": "false",

        "SIFT/NFeatures": "0",
        "SIFT/NOctaveLayers": "4",

        "FREAK/OrientationNormalized": "true",
        "FREAK/ScaleNormalized": "true",

        "KAZE/Extended": "false",
        "KAZE/Upright": "false",

        "Vis/CorGuessWinSize": "40",
        # 0=Features Matching, 1=Optical Flow
        "Vis/CorType": "1",
        "Vis/MaxFeatures": "1000",
        # "Vis/MinDepth": "0.0",
        # "Vis/MaxDepth": "3.0",
    }]

    remappings = [
        ("rgb/image", "camera/color/image_raw"),
        ("rgb/camera_info", "camera/color/camera_info"),
        ("depth/image", "camera/aligned_depth_to_color/image_raw"),
        ("imu", "imu"),
        ("odom", "odom_rgbd")]

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
