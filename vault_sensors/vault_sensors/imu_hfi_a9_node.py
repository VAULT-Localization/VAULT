#!/usr/bin/env python3

import math
import serial
import struct
import binascii

from typing import List

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField


class ImuHfiA9Node(Node):

    def __init__(self) -> None:
        super().__init__("imu_hfi_a9_node")

        # params
        self.declare_parameter("frame_id", "imu_link")
        self.frame_id = self.get_parameter(
            "frame_id").get_parameter_value().string_value

        self.declare_parameter("update_rate", 300)
        self.update_rate = self.get_parameter(
            "update_rate").get_parameter_value().integer_value

        self.declare_parameter("read_rate", 1000)
        self.read_rate = self.get_parameter(
            "read_rate").get_parameter_value().integer_value

        self.declare_parameter("device", "/dev/ttyUSB0")
        self.usb_port = self.get_parameter(
            "device").get_parameter_value().string_value

        self.declare_parameter("baud", 921600)
        self.baudrate = self.get_parameter(
            "baud").get_parameter_value().integer_value

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

        # pubs
        self.imu_pub = self.create_publisher(Imu, "imu", 10)
        self.mag_pub = self.create_publisher(MagneticField, "mag", 10)

        # aux
        self._sensor_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._rpy_degree = [0, 0, 0]

        # starts
        self.open_device(self.usb_port, self.baudrate)
        self.create_timer(1 / self.read_rate, self.read_data)
        self.create_timer(1 / self.update_rate, self.publish_data)

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
    def eul_to_qua(euler: List[float]) -> Quaternion:
        eular_div = [0, 0, 0]
        eular_div[0], eular_div[1], eular_div[2] = euler[0] / \
            2.0, euler[1] / 2.0, euler[2] / 2.0

        ca, cb, cc = math.cos(eular_div[0]), math.cos(
            eular_div[1]), math.cos(eular_div[2])
        sa, sb, sc = math.sin(eular_div[0]), math.sin(
            eular_div[1]), math.sin(eular_div[2])

        x = sa * cb * cc - ca * sb * sc
        y = ca * sb * cc + sa * cb * sc
        z = ca * cb * sc - sa * sb * cc
        w = ca * cb * cc + sa * sb * sc

        orientation = Quaternion()
        orientation.x, orientation.y, orientation.z, orientation.w = x, y, z, w
        return orientation

    @staticmethod
    def receive_split(buffer: bytearray) -> List[bytes]:
        new_buffer = []
        for i in range(0, len(buffer), 2):
            new_buffer.append(buffer[i:i + 2])
        return new_buffer

    @staticmethod
    def hex_to_ieee(size: int, buffer: List[bytes]) -> List[float]:
        aux = ""
        data = []

        for i in range(int(size / 2 - 3), 11, -4):
            for j in range(i, i - 4, -1):
                aux += buffer[j].decode("utf-8")
            aux = bytes.fromhex(aux)
            data.append(struct.unpack(">f", aux)[0])
            aux = ""

        data.reverse()
        return data

    def read_data(self) -> None:

        # check if there are data
        count = self.hf_imu.inWaiting()

        if count > 24:
            # read data
            receive_buffer = bytearray()
            receive_buffer = binascii.b2a_hex(self.hf_imu.read(count))
            receive_len = len(receive_buffer)
            buffer = self.receive_split(receive_buffer)

            # parse sensors data
            if (buffer[0] + buffer[1] + buffer[2]).decode("utf-8") == "aa552c":
                self._sensor_data = self.hex_to_ieee(receive_len, buffer)

            # parse orientation
            if (buffer[0] + buffer[1] + buffer[2]).decode("utf-8") == "aa5514":
                rpy = self.hex_to_ieee(receive_len, buffer)
                self._rpy_degree[0] = rpy[0] / 180 * math.pi
                self._rpy_degree[1] = rpy[1] / -180 * math.pi
                self._rpy_degree[2] = rpy[2] / -180 * math.pi

    def publish_data(self) -> None:
        stamp = self.get_clock().now().to_msg()

        # IMU msg
        imu_msg = Imu()

        imu_msg.header.stamp = stamp
        imu_msg.header.frame_id = self.frame_id

        imu_msg.orientation = self.eul_to_qua(self._rpy_degree)
        imu_msg.orientation_covariance = self.orientation_covariance

        imu_msg.angular_velocity.x = float(self._sensor_data[0])
        imu_msg.angular_velocity.y = float(self._sensor_data[1])
        imu_msg.angular_velocity.z = float(self._sensor_data[2])
        imu_msg.angular_velocity_covariance = self.angular_velocity_covariance

        imu_msg.linear_acceleration.x = float(
            self._sensor_data[3] * -9.8)
        imu_msg.linear_acceleration.y = float(
            self._sensor_data[4] * -9.8)
        imu_msg.linear_acceleration.z = float(
            self._sensor_data[5] * -9.8)
        imu_msg.linear_acceleration_covariance = self.linear_acceleration_covariance

        self.imu_pub.publish(imu_msg)

        # magnetic msg
        mag_msg = MagneticField()
        mag_msg.header.stamp = stamp
        mag_msg.header.frame_id = self.frame_id
        mag_msg.magnetic_field.x = float(self._sensor_data[6])
        mag_msg.magnetic_field.y = float(self._sensor_data[7])
        mag_msg.magnetic_field.z = float(self._sensor_data[8])
        mag_msg.magnetic_field_covariance = self.magnetic_field_covariance

        self.mag_pub.publish(mag_msg)


def main(args=None):
    rclpy.init(args=args)

    node = ImuHfiA9Node()
    rclpy.spin(node)
    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
