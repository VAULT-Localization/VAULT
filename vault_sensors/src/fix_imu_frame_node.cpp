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

#define BOOST_BIND_NO_PLACEHOLDERS

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"

#include "vault_sensors/fix_imu_frame_node.hpp"

using std::placeholders::_1;

FixImuFrameNode::FixImuFrameNode() : rclcpp::Node("fix_imu_frame_node") {

  this->declare_parameter<std::string>("new_frame", "imu_optical_frame");
  this->get_parameter("new_frame", this->new_frame);

  this->declare_parameter<std::string>("frame_prefix", "camera");
  this->get_parameter("frame_prefix", this->frame_prefix);

  this->pub = this->create_publisher<sensor_msgs::msg::Imu>("imu", 10);
  this->sub = this->create_subscription<sensor_msgs::msg::Imu>(
      "imu/data", 10, std::bind(&FixImuFrameNode::callback, this, _1));
}

void FixImuFrameNode::callback(const sensor_msgs::msg::Imu::SharedPtr msg) {
  msg->header.frame_id = this->frame_prefix + "_" + this->new_frame;
  this->pub->publish(*msg);
}

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<FixImuFrameNode>());
  rclcpp::shutdown();
  return 0;
}