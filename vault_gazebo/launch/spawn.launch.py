import os
from ament_index_python import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution


def generate_launch_description():

    ### ARGS ###
    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace",
        default_value="vault",
        description="Vault namespace")

    initial_pose_x = LaunchConfiguration("initial_pose_x")
    initial_pose_x_cmd = DeclareLaunchArgument(
        "initial_pose_x",
        default_value="0.0",
        description="Initial pose x")

    initial_pose_y = LaunchConfiguration("initial_pose_y")
    initial_pose_y_cmd = DeclareLaunchArgument(
        "initial_pose_y",
        default_value="0.0",
        description="Initial pose y")

    initial_pose_z = LaunchConfiguration("initial_pose_z")
    initial_pose_z_cmd = DeclareLaunchArgument(
        "initial_pose_z",
        default_value="0.0",
        description="Initial pose z")

    initial_pose_yaw = LaunchConfiguration("initial_pose_yaw")
    initial_pose_yaw_cmd = DeclareLaunchArgument(
        "initial_pose_yaw",
        default_value="0.0",
        description="Initial pose yaw")

    ### XACRO ###
    xacro_file = os.path.join(get_package_share_directory(
        "vault_description"), "robots/vault.urdf.xacro")
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            xacro_file,
            " ",
            "prefix:=", namespace
        ]
    )

    params = {"robot_description": robot_description_content,
              "use_sim_time": True,
              "frame_prefix": [namespace, "/"]}

    ### NODES ###
    robot_state_publisher_cmd = Node(
        name="robot_state_publisher",
        namespace=namespace,
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[params]
    )

    spawn_entity_cmd = Node(
        package="gazebo_ros",
        namespace=namespace,
        executable="spawn_entity.py",
        arguments=["-entity", namespace,
                   "-topic", "robot_description",
                   "-timeout", "120",
                   "-robot_namespace", namespace,
                   "-x", initial_pose_x,
                   "-y", initial_pose_y,
                   "-z", initial_pose_z,
                   "-Y", initial_pose_yaw],
        output="screen",
        parameters=[{"use_sim_time": True}]
    )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(initial_pose_x_cmd)
    ld.add_action(initial_pose_y_cmd)
    ld.add_action(initial_pose_z_cmd)
    ld.add_action(initial_pose_yaw_cmd)

    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_entity_cmd)

    return ld
