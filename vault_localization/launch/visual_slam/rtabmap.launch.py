# Copyright (C) 2023 Miguel Ángel González Santamarta

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from launch import LaunchDescription, LaunchContext
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PythonExpression


def generate_launch_description():

    def run_rtabmap(
        context: LaunchContext,
        namespace,
        use_sim_time,
        publish_visual_slam_tf,
        use_t265,
        use_gps,
    ):

        use_gps = str(context.perform_substitution(use_gps))

        parameters = [
            {
                "frame_id": "base_link",
                "map_frame_id": "map",
                "subscribe_depth": PythonExpression(["not ", use_t265]),
                "subscribe_rgb": PythonExpression(["not ", use_t265]),
                "subscribe_stereo": use_t265,
                "subscribe_scan": False,
                "subscribe_odom": True,
                "subscribe_odom_info": False,
                "odom_sensor_sync": True,
                "approx_sync": True,
                "publish_tf": publish_visual_slam_tf,
                "use_sim_time": use_sim_time,
                "qos_image": 2,
                "qos_camera_info": 2,
                "qos_gps": 2,
                "qos_imu": 2,
                "qos_scan": 2,
                "queue_size": 30,
                "Rtabmap/LoopGPS": use_gps,
                # 0=TORO, 1=g2o, 2=GTSAM and 3=Ceres
                "Optimizer/Strategy": "2",
                "Optimizer/GravitySigma": "0.3",
                "RGBD/Enabled": "true",
                "RGBD/OptimizeMaxError": "3.0",
                "RGBD/OptimizeFromGraphEnd": "true",
                "RGBD/CreateOccupancyGrid": "true",
                "RGBD/LoopClosureIdentityGuess": "true",
                "RGBD/LocalBundleOnLoopClosure": "true",
                "VhEp/Enabled": "true",
                "Rtabmap/CreateIntermediateNodes": "false",
                "GFTT/MinDistance": "7.0",
                "GFTT/QualityLevel": "0.001",
                "GFTT/BlockSize": "3",
                "GFTT/UseHarrisDetector": "true",
                "GFTT/K": "0.04",
                "BRIEF/Bytes": "64",
                # Motion estimation approach: 0:3D->3D, 1:3D->2D (PnP), 2:2D->2D (Epipolar Geometry)
                "Vis/EstimationType": "1",
                "Vis/ForwardEstOnly": "true",
                # 0=SURF 1=SIFT 2=ORB 3=FAST/FREAK 4=FAST/BRIEF 5=GFTT/FREAK 6=GFTT/BRIEF 7=BRISK 8=GFTT/ORB 9=KAZE 10=ORB-OCTREE 11=SuperPoint 12=SURF/FREAK 13=GFTT/DAISY 14=SURF/DAISY 15=PyDetector
                "Vis/FeatureType": "8",
                "Vis/DepthAsMask": "true",
                "Vis/CorGuessWinSize": "40",
                "Vis/MaxFeatures": "1000",
                "Vis/MinDepth": "0.2",
                "Vis/MaxDepth": "0.0",
                # 0=Features Matching, 1=Optical Flow
                "Vis/CorType": "0",
                # kNNFlannNaive=0, kNNFlannKdTree=1, kNNFlannLSH=2, kNNBruteForce=3, kNNBruteForceGPU=4, BruteForceCrossCheck=5, SuperGlue=6, GMS=7
                "Vis/CorNNType": "1",
                "Grid/Sensor": "1",
                "Grid/DepthDecimation": "4",
                "Grid/RangeMin": "0.0",
                "Grid/RangeMax": "3.0",
                "Grid/MinClusterSize": "10",
                "Grid/MaxGroundAngle": "45",
                "Grid/NormalK": "20",
                "Grid/ClusterRadius": "0.1",
                "Grid/CellSize": "0.05",
                "Grid/FlatObstacleDetected": "false",
                "Grid/RayTracing": "true",
                "Grid/3D": "true",
                "Grid/MapFrameProjection": "true",
                "GridGlobal/UpdateError": "0.01",
                "GridGlobal/MinSize": "100.0",
                "GridGlobal/Eroded": "true",
                "GridGlobal/FloodFillDepth": "16",
            }
        ]

        remappings = [
            # subs
            ("rgb/image", "d435i/color/image_raw"),
            ("rgb/camera_info", "d435i/color/camera_info"),
            ("depth/image", "d435i/depth/image_rect_raw"),
            ("imu", "imu"),
            ("odom", "odom"),
            ("odom_info", "odom_info"),
            ("goal", "goal_pose"),
            ("gps/fix", "gps/fix"),
            ("left/image_rect", "t265/fisheye1/image_raw"),
            ("left/camera_info", "t265/fisheye1/camera_info"),
            ("right/image_rect", "t265/fisheye2/image_raw"),
            ("right/camera_info", "t265/fisheye2/camera_info"),
        ]

        return (
            Node(
                package="rtabmap_slam",
                executable="rtabmap",
                output="screen",
                namespace=namespace,
                parameters=parameters,
                remappings=remappings,
                arguments=["-d", "--ros-args", "--log-level", "Warn"],
            ),
        )

    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace", default_value="vault", description="Vault namespace"
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time",
        default_value="False",
        description="Use simulation (Gazebo) clock if True",
    )

    publish_visual_slam_tf = LaunchConfiguration("publish_visual_slam_tf")
    publish_visual_slam_tf_cmd = DeclareLaunchArgument(
        "publish_visual_slam_tf",
        default_value="True",
        description="Wheter to publish visual SLAM tf map or EKF one",
    )

    use_t265 = LaunchConfiguration("use_t265")
    use_t265_cmd = DeclareLaunchArgument(
        "use_t265",
        default_value="False",
        description="Wheter to use T265 camera or D435i for visual SLAM",
    )

    use_gps = LaunchConfiguration("use_gps")
    use_gps_cmd = DeclareLaunchArgument(
        "use_gps",
        default_value="True",
        description="Wheter to use GPS data in the loop clousure",
    )

    return LaunchDescription(
        [
            namespace_cmd,
            use_sim_time_cmd,
            publish_visual_slam_tf_cmd,
            use_t265_cmd,
            use_gps_cmd,
            OpaqueFunction(
                function=run_rtabmap,
                args=[namespace, use_sim_time, publish_visual_slam_tf, use_t265, use_gps],
            ),
        ]
    )
