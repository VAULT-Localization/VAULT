import os
from ament_index_python import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch import LaunchDescription
import xacro


def generate_launch_description():

    ### ARGS ###
    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace",
        default_value="vault",
        description="Vault namespace")

    ### XACRO ###
    xacro_file = os.path.join(get_package_share_directory(
        "vault_description"), "robots/vault.urdf.xacro")
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    params = {"robot_description": doc.toxml(), "use_sim_time": True}

    ### NODES ###
    robot_state_publisher_cmd = Node(
        name="robot_state_publisher",
        namespace=namespace,
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[params]
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(robot_state_publisher_cmd)

    return ld
