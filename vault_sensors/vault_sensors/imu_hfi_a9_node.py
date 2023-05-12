#!/usr/bin/env python3

import math
import serial
import struct

from typing import List

import rclpy
from rclpy.node import Node

from tf_transformations import quaternion_from_euler

from rclpy.qos import QoSProfile
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSReliabilityPolicy

from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField


class ImuHfiA9Node(Node):

    def __init__(self) -> None:
        super().__init__("imu_hfi_a9_node")

        # params
        self.declare_parameter("frame_id", "imu_link")
        self.frame_id = self.get_parameter(
            "frame_id").get_parameter_value().string_value

        self.declare_parameter("device", "/dev/ttyUSB0")
        self.usb_port = self.get_parameter(
            "device").get_parameter_value().string_value

        self.declare_parameter("baud", 921600)
        self.baudrate = self.get_parameter(
            "baud").get_parameter_value().integer_value

        self.declare_parameter("gravitacional_normalization", True)
        self.gravitacional_normalization = self.get_parameter(
            "gravitacional_normalization").get_parameter_value().bool_value

        self.declare_parameter("orientation_covariance", [
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.orientation_covariance = self.get_parameter(
            "orientation_covariance").get_parameter_value().double_array_value.tolist()

        self.declare_parameter("angular_velocity_covariance", [
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.angular_velocity_covariance = self.get_parameter(
            "angular_velocity_covariance").get_parameter_value().double_array_value.tolist()

        self.declare_parameter("linear_acceleration_covariance", [
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.linear_acceleration_covariance = self.get_parameter(
            "linear_acceleration_covariance").get_parameter_value().double_array_value.tolist()

        self.declare_parameter("magnetic_field_covariance", [
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.magnetic_field_covariance = self.get_parameter(
            "magnetic_field_covariance").get_parameter_value().double_array_value.tolist()

        # aux
        self.orientation = [0.0, 0.0, 0.0, 0.0]
        self.angular_velocity = [0.0, 0.0, 0.0]
        self.linear_acceleration = [0.0, 0.0, 0.0]
        self.magnetometer = [0.0, 0.0, 0.0]

        # pubs
        sensor_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.VOLATILE,
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            depth=10
        )

        self.imu_pub = self.create_publisher(Imu, "imu", sensor_qos)
        self.mag_pub = self.create_publisher(MagneticField, "mag", sensor_qos)

        # starts
        self.open_device(self.usb_port, self.baudrate)
        self.create_timer(1 / 1000, self.work)

    def open_device(self, usb_port: str, baudrate: int, timeout: float = 0.5) -> None:
        try:
            self.hf_imu = serial.Serial(port=usb_port,
                                        baudrate=baudrate,
                                        timeout=timeout)
            if self.hf_imu.isOpen():
                self.get_logger().info("IMU is already open")
            else:
                self.hf_imu.open()
                self.get_logger().info("IMU is open")

        except Exception as e:
            self.get_logger().error(str(e))
            exit()

    @staticmethod
    def check_sum(raw_data: List[int], check_data: List[int]) -> bool:
        data = bytearray(raw_data)
        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for _ in range(8):
                if (crc & 1) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return hex(((crc & 0xff) << 8) + (crc >> 8)) == hex(check_data[0] << 8 | check_data[1])

    @staticmethod
    def hex_to_ieee(raw_data: List[int]) -> List[float]:
        ieee_data = []
        raw_data.reverse()
        for i in range(0, len(raw_data), 4):
            data2str = (
                hex(raw_data[i] | 0xff00)[4:6] +
                hex(raw_data[i + 1] | 0xff00)[4:6] +
                hex(raw_data[i + 2] | 0xff00)[4:6] +
                hex(raw_data[i + 3] | 0xff00)[4:6]
            )
            ieee_data.append(struct.unpack('>f', bytes.fromhex(data2str))[0])
        ieee_data.reverse()
        return ieee_data

    def work(self) -> None:
        count = self.hf_imu.inWaiting()

        if count > 0:
            try:
                buff_data = self.hf_imu.read(count)
                self.handle_data(list(buff_data))
            except serial.SerialException as e:
                self.get_logger().error(
                    "Error reading from serial: {:s}".format(str(e)))

    def handle_data(self, raw_data: List[int]) -> None:

        # check header
        if raw_data[0] != 0xaa:
            return
        if raw_data[1] != 0x55:
            return

        # check msg type
        if raw_data[2] == 0x2c:

            if self.check_sum(raw_data[2:47], raw_data[47:49]):
                data = self.hex_to_ieee(raw_data[7:47])
                self.angular_velocity = data[1:4]
                self.linear_acceleration = data[4:7]
                self.magnetometer = data[7:10]
            else:
                self.get_logger().error("Check Sum verification failed")
                return

        elif raw_data[2] == 0x14:

            if self.check_sum(raw_data[2:23], raw_data[23:25]):
                data = self.hex_to_ieee(raw_data[7:23])
                aux_orientation = data[1:4]
                aux_orientation = [aux_orientation[i]
                                   * math.pi / 180 for i in range(3)]
                self.orientation = quaternion_from_euler(
                    aux_orientation[0], -aux_orientation[1], -aux_orientation[2])
            else:
                self.get_logger().error("Check Sum verification failed")
                return

        # publish
        stamp = self.get_clock().now().to_msg()

        imu_msg = Imu()
        imu_msg.header.stamp = stamp
        imu_msg.header.frame_id = self.frame_id

        imu_msg.orientation.x = self.orientation[0]
        imu_msg.orientation.y = self.orientation[1]
        imu_msg.orientation.z = self.orientation[2]
        imu_msg.orientation.w = self.orientation[3]
        imu_msg.orientation_covariance = self.orientation_covariance

        imu_msg.angular_velocity.x = self.angular_velocity[0]
        imu_msg.angular_velocity.y = self.angular_velocity[1]
        imu_msg.angular_velocity.z = self.angular_velocity[2]
        imu_msg.angular_velocity_covariance = self.angular_velocity_covariance

        acc_k = math.sqrt(
            self.linear_acceleration[0] ** 2 +
            self.linear_acceleration[1] ** 2 +
            self.linear_acceleration[2] ** 2
        )
        if acc_k == 0:
            acc_k = 1
        if self.gravitacional_normalization:
            imu_msg.linear_acceleration.x = self.linear_acceleration[0] * -9.8 / acc_k
            imu_msg.linear_acceleration.y = self.linear_acceleration[1] * -9.8 / acc_k
            imu_msg.linear_acceleration.z = self.linear_acceleration[2] * -9.8 / acc_k
        else:
            imu_msg.linear_acceleration.x = self.linear_acceleration[0] * -9.8
            imu_msg.linear_acceleration.y = self.linear_acceleration[1] * -9.8
            imu_msg.linear_acceleration.z = self.linear_acceleration[2] * -9.8
        imu_msg.linear_acceleration_covariance = self.linear_acceleration_covariance

        self.imu_pub.publish(imu_msg)

        # mag
        mag_msg = MagneticField()
        mag_msg.header.stamp = stamp
        mag_msg.header.frame_id = self.frame_id

        mag_msg.magnetic_field.x = self.magnetometer[0]
        mag_msg.magnetic_field.y = self.magnetometer[1]
        mag_msg.magnetic_field.z = self.magnetometer[2]

        self.mag_pub.publish(mag_msg)


def main(args=None):
    rclpy.init(args=args)

    node = ImuHfiA9Node()
    rclpy.spin(node)
    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
