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


import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    pkg_path = get_package_share_directory("vault_visualization")

    rviz_config = os.path.join(pkg_path, "rviz", "default.rviz")

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time",
        default_value="False",
        description="Use simulation (Gazebo) clock if True",
    )

    # repub_cmd = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(get_package_share_directory("vault_visualization"),
    #                      "launch", "republish.launch.py")
    #     ),
    #     launch_arguments={
    #         "namespace": "vault",
    #         "repub_rgb": "True",
    #         "repub_depth": "False",
    #         "repub_infras": "False",
    #         "repub_fisheyes": "False"
    #     }.items()
    # )

    rviz_cmd = Node(
        name="rviz",
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_config],
        parameters=[{"use_sim_time": use_sim_time}],
    )

    ld = LaunchDescription()
    ld.add_action(use_sim_time_cmd)
    # ld.add_action(repub_cmd)
    ld.add_action(rviz_cmd)
    return ld
