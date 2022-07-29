import os
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import AnyLaunchDescriptionSource


def generate_launch_description():

    return LaunchDescription([


        ExecuteProcess(
            cmd=["foxglove-studio"],
            log_cmd=True,
            sigterm_timeout="0",
            sigkill_timeout="0",
            on_exit=[]
        ),

        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(
                os.path.join(get_package_share_directory("rosbridge_server"),
                             "launch", "rosbridge_websocket_launch.xml")
            )
        ),

    ])
