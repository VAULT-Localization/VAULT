
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument


def generate_launch_description():

    namespace = LaunchConfiguration("namespace")
    namespace_cmd = DeclareLaunchArgument(
        "namespace",
        default_value="vault",
        description="Vault namespace")

    frame_id = LaunchConfiguration("frame_id")
    frame_id_cmd = DeclareLaunchArgument(
        "frame_id",
        default_value=[namespace, "_imu_link"],
        description="frame_id")

    update_rate = LaunchConfiguration("update_rate")
    update_rate_cmd = DeclareLaunchArgument(
        "update_rate",
        default_value="300",
        description="update rate")

    read_rate = LaunchConfiguration("read_rate")
    read_rate_cmd = DeclareLaunchArgument(
        "read_rate",
        default_value="1000",
        description="read rate from serial")

    device = LaunchConfiguration("device")
    device_cmd = DeclareLaunchArgument(
        "device",
        default_value="/dev/ttyUSB0",
        description="USB device")

    baud = LaunchConfiguration("baud")
    baud_cmd = DeclareLaunchArgument(
        "baud",
        default_value="921600",
        description="baud rate")

    orientation_covariance = LaunchConfiguration("orientation_covariance")
    orientation_covariance_cmd = DeclareLaunchArgument(
        "orientation_covariance",
        default_value="[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]",
        description="Covariance for IMU orientation")

    angular_velocity_covariance = LaunchConfiguration(
        "angular_velocity_covariance")
    angular_velocity_covariance_cmd = DeclareLaunchArgument(
        "angular_velocity_covariance",
        default_value="[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]",
        description="Covariance for IMU angualar velocity")

    linear_acceleration_covariance = LaunchConfiguration(
        "linear_acceleration_covariance")
    linear_acceleration_covariance_cmd = DeclareLaunchArgument(
        "linear_acceleration_covariance",
        default_value="[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]",
        description="Covariance for IMU linar acceleration")

    magnetic_field_covariance = LaunchConfiguration(
        "magnetic_field_covariance")
    magnetic_field_covariance_cmd = DeclareLaunchArgument(
        "magnetic_field_covariance",
        default_value="[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]",
        description="Covariance for magnetic field")

    imu_hfi_a9_node = Node(package="vault_sensors",
                           executable="imu_hfi_a9_node",
                           namespace=namespace,
                           output="both",
                           parameters=[
                               {
                                   "frame_id": frame_id,
                                   "update_rate": update_rate,
                                   "read_rate": read_rate,
                                   "device": device,
                                   "baud": baud,
                                   "orientation_covariance": orientation_covariance,
                                   "angular_velocity_covariance": angular_velocity_covariance,
                                   "linear_acceleration_covariance": linear_acceleration_covariance,
                                   "magnetic_field_covariance": magnetic_field_covariance
                               }
                           ]
                           )

    ld = LaunchDescription()

    ld.add_action(namespace_cmd)
    ld.add_action(frame_id_cmd)
    ld.add_action(update_rate_cmd)
    ld.add_action(read_rate_cmd)
    ld.add_action(device_cmd)
    ld.add_action(baud_cmd)
    ld.add_action(orientation_covariance_cmd)
    ld.add_action(angular_velocity_covariance_cmd)
    ld.add_action(linear_acceleration_covariance_cmd)
    ld.add_action(magnetic_field_covariance_cmd)

    ld.add_action(imu_hfi_a9_node)

    return ld
