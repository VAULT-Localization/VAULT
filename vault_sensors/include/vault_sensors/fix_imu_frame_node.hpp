#ifndef FIX_IMU_FRAME_HPP
#define FIX_IMU_FRAME_HPP

#include <string>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"

class FixImuFrameNode : public rclcpp::Node {
public:
  FixImuFrameNode();
  void callback(const sensor_msgs::msg::Imu::SharedPtr msg);

private:
  std::string new_frame;
  std::string frame_prefix;

  rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr sub;
  rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr pub;
};

#endif