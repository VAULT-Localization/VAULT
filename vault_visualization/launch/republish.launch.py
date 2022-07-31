from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.conditions import IfCondition


def generate_launch_description():

    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace",
        default_value="vault",
        description="Vault namespace")

    repub_rgb = LaunchConfiguration("repub_rgb")
    repub_rgb_cmd = DeclareLaunchArgument(
        "repub_rgb",
        default_value="True",
        description="Whether repub RGB compressed topic")

    repub_depth = LaunchConfiguration("repub_depth")
    repub_depth_cmd = DeclareLaunchArgument(
        "repub_depth",
        default_value="False",
        description="Whether repub depth compressed topic")

    repub_infras = LaunchConfiguration("repub_infras")
    repub_infras_cmd = DeclareLaunchArgument(
        "repub_infras",
        default_value="False",
        description="Whether repub infras compressed topics")

    repub_fisheyes = LaunchConfiguration("repub_fisheyes")
    repub_fisheyes_cmd = DeclareLaunchArgument(
        "repub_fisheyes",
        default_value="False",
        description="Whether repub fisheyes compressed topics")

    return LaunchDescription([
        namespace_cmd,
        repub_rgb_cmd,
        repub_depth_cmd,
        repub_infras_cmd,
        repub_fisheyes_cmd,


        # rgbd
        Node(
            package="vault_visualization",
            executable="republish_node",
            name="rgb_republish_node",
            remappings=[
                ("in/compressed", "d435i/color/image_raw/compressed"),
                ("out", "d435i/color/image_raw/repub")],
            arguments=["compressed", "raw"],
            namespace=namespace,
            condition=IfCondition(PythonExpression([repub_rgb]))
        ),

        Node(
            package="vault_visualization",
            executable="republish_node",
            name="depth_republish_node",
            remappings=[
                ("in/compressedDepth",
                 "d435i/aligned_depth_to_color/image_raw/compressedDepth"),
                ("out", "d435i/aligned_depth_to_color/image_raw/repub")],
            arguments=["compressedDepth", "raw"],
            namespace=namespace,
            condition=IfCondition(PythonExpression([repub_depth]))
        ),

        # infra
        Node(
            package="vault_visualization",
            executable="republish_node",
            name="infra1_republish_node",
            remappings=[
                ("in/compressed", "d435i/infra1/image_rect_raw/compressed"),
                ("out", "d435i/infra1/image_rect_raw/repub")],
            arguments=["compressed", "raw"],
            namespace=namespace,
            condition=IfCondition(PythonExpression([repub_infras]))
        ),

        Node(
            package="vault_visualization",
            executable="republish_node",
            name="infra2_republish_node",
            remappings=[
                ("in/compressed", "d435i/infra2/image_rect_raw/compressed"),
                ("out", "d435i/infra2/image_rect_raw/repub")],
            arguments=["compressed", "raw"],
            namespace=namespace,
            condition=IfCondition(PythonExpression([repub_infras]))
        ),

        # fisheye
        Node(
            package="vault_visualization",
            executable="republish_node",
            name="fisheye1_republish_node",
            remappings=[
                ("in/compressed", "t265/fisheye1/image_raw/compressed"),
                ("out", "t265/fisheye1/image_raw/repub")],
            arguments=["compressed", "raw"],
            namespace=namespace,
            condition=IfCondition(PythonExpression([repub_fisheyes]))
        ),

        Node(
            package="vault_visualization",
            executable="republish_node",
            name="fisheye2_republish_node",
            remappings=[
                ("in/compressed", "t265/fisheye2/image_raw/compressed"),
                ("out", "t265/fisheye2/image_raw/repub")],
            arguments=["compressed", "raw"],
            namespace=namespace,
            condition=IfCondition(PythonExpression([repub_fisheyes]))
        ),

    ])
