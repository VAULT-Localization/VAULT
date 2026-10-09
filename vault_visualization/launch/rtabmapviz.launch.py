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


from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression


def generate_launch_description():

    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace",
        default_value="vault",
        description="Vault namespace",
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time",
        default_value="False",
        description="Use simulation (Gazebo) clock if True",
    )

    use_t265 = LaunchConfiguration("use_t265")
    use_t265_cmd = DeclareLaunchArgument(
        "use_t265",
        default_value="False",
        description="Wheter to use T265 camera or D435i for visual SLAM",
    )

    parameters = [
        {
            "frame_id": "base_link",
            "odom_frame_id": "odom",
            "map_frame_id": "map",
            "subscribe_depth": PythonExpression(["not ", use_t265]),
            "subscribe_rgb": PythonExpression(["not ", use_t265]),
            "subscribe_stereo": use_t265,
            "subscribe_scan": False,
            "subscribe_odom_info": False,
            "approx_sync": True,
            "use_sim_time": use_sim_time,
            "qos_image": 2,
            "qos_camera_info": 2,
            "qos_gps": 2,
            "qos_imu": 2,
            "qos_scan": 2,
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

    return LaunchDescription(
        [
            namespace_cmd,
            use_sim_time_cmd,
            use_t265_cmd,
            # IncludeLaunchDescription(
            #     PythonLaunchDescriptionSource(
            #         os.path.join(get_package_share_directory("vault_visualization"),
            #                      "launch", "republish.launch.py")
            #     ),
            #     launch_arguments={
            #         "namespace": namespace,
            #         "repub_rgb": PythonExpression(["not ", use_t265]),
            #         "repub_depth": "False",
            #         "repub_infras": "False",
            #         "repub_fisheyes": use_t265
            #     }.items()
            # ),
            Node(
                package="rtabmap_viz",
                executable="rtabmap_viz",
                output="screen",
                namespace=namespace,
                parameters=parameters,
                remappings=remappings,
            ),
        ]
    )
