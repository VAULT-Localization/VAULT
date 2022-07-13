from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    parameters = [{
        "frame_id": "vault_base_link",
        "odom_frame_id": "vault_odom",
        "subscribe_depth": True,
        "subscribe_rgb": True,
        "approx_sync": True,
        "publish_tf": False,
        "wait_imu_to_init": False,
        "publish_null_when_lost": False,
        "qos": 2,
        "qos_camera_info": 2,

        "Optimizer/Strategy": "2",
        "Optimizer/GravitySigma": "0.0",

        "Odom/Strategy": "0",
        "Odom/ResetCountdown": "10",
        "Odom/Holonomic": "false",
        "Odom/FilteringStrategy": "0",
        "Odom/ParticleSize": "500",

        "GFTT/MinDistance": "7",
        "GFTT/QualityLevel": "0.1",

        "SURF/Extended": "true",
        "SURF/Upright": "true",

        "SIFT/NFeatures": "500",
        "SIFT/NOctaveLayers": "5",

        "FREAK/OrientationNormalized": "true",
        "FREAK/ScaleNormalized": "true",

        "KAZE/Extended": "true",
        "KAZE/Upright": "true",

        "Vis/CorGuessWinSize": "40",
        "Vis/CorType": "0",
        "Vis/MaxFeatures": "1000",
        "Vis/MinDepth": "0.0",
        "Vis/MaxDepth": "3.0",

        "Mem/ImageKept": "true",
        "Mem/STMSize": "100",
        "Mem/IncrementalMemory": "true",
        "FAST/CV": "10"
    }]

    remappings = [
        ("rgb/image", "camera/color/image_raw"),
        ("rgb/camera_info", "camera/color/camera_info"),
        ("depth/image", "camera/aligned_depth_to_color/image_raw"),
        ("imu", "imu"),
        ("odom", "odom_rgbd")]

    return LaunchDescription([
        DeclareLaunchArgument(
            "namespace",
            default_value="vault",
            description="Vault namespace"),

        Node(
            package="rtabmap_ros",
            executable="rgbd_odometry",
            output="log",
            namespace=LaunchConfiguration("namespace"),
            parameters=parameters,
            remappings=remappings,
            arguments=["--ros-args", "--log-level", "Warn"]),
    ])
