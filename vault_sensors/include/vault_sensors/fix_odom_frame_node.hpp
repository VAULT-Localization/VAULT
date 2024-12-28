// Copyright (C) 2023 Miguel Ángel González Santamarta

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

#ifndef FIX_ODOM_FRAME_HPP
#define FIX_ODOM_FRAME_HPP

#include <string>

#include <nav_msgs/msg/odometry.hpp>
#include <rclcpp/rclcpp.hpp>

#include <tf2/exceptions.h>
#include <tf2_ros/buffer.h>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2_ros/transform_listener.h>

class FixOdomFrameNode : public rclcpp::Node {
public:
  FixOdomFrameNode();
  void callback(const nav_msgs::msg::Odometry::SharedPtr msg);

private:
  std::string frame_id;
  std::string odom_frame;
  bool publish_tf;

  std::shared_ptr<tf2_ros::TransformListener> transform_listener{nullptr};
  std::unique_ptr<tf2_ros::Buffer> tf_buffer;
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster;

  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr sub;
  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr pub;
};

#endif