// Copyright (C) 2023  Miguel Ángel González Santamarta

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

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