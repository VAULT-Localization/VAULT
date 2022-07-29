from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression


def generate_launch_description():

    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace",
        default_value="vault",
        description="Vault namespace")

    return LaunchDescription([
        namespace_cmd,

        # rgbd
        Node(
            package="vault_visualization",
            executable="republish_node",
            name="rgb_republish_node",
            remappings=[
                ("in/compressed", "d435i/color/image_raw/compressed"),
                ("out", "d435i/color/image_raw/repub")],
            arguments=["compressed", "raw"],
            namespace=namespace),

        Node(
            package="vault_visualization",
            executable="republish_node",
            name="depth_republish_node",
            remappings=[
                ("in/compressedDepth",
                 "d435i/aligned_depth_to_color/image_raw/compressedDepth"),
                ("out", "d435i/aligned_depth_to_color/image_raw/repub")],
            arguments=["compressedDepth", "raw"],
            namespace=namespace),

        # infra
        Node(
            package="vault_visualization",
            executable="republish_node",
            name="infra1_republish_node",
            remappings=[
                ("in/compressed", "d435i/infra1/image_rect_raw/compressed"),
                ("out", "d435i/infra1/image_rect_raw/repub")],
            arguments=["compressed", "raw"],
            namespace=namespace),

        Node(
            package="vault_visualization",
            executable="republish_node",
            name="infra2_republish_node",
            remappings=[
                ("in/compressed", "d435i/infra2/image_rect_raw/compressed"),
                ("out", "d435i/infra2/image_rect_raw/repub")],
            arguments=["compressed", "raw"],
            namespace=namespace),

        # fisheye
        Node(
            package="vault_visualization",
            executable="republish_node",
            name="fisheye1_republish_node",
            remappings=[
                ("in/compressed", "t265/fisheye1/image_raw/compressed"),
                ("out", "t265/fisheye1/image_raw/repub")],
            arguments=["compressed", "raw"],
            namespace=namespace),

        Node(
            package="vault_visualization",
            executable="republish_node",
            name="fisheye2_republish_node",
            remappings=[
                ("in/compressed", "t265/fisheye2/image_raw/compressed"),
                ("out", "t265/fisheye2/image_raw/repub")],
            arguments=["compressed", "raw"],
            namespace=namespace),

    ])
