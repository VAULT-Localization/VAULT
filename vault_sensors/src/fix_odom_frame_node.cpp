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

#define BOOST_BIND_NO_PLACEHOLDERS

#include <cmath>

#include <geometry_msgs/msg/pose_with_covariance_stamped.hpp>
#include <geometry_msgs/msg/transform_stamped.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <rclcpp/rclcpp.hpp>

#include <tf2/LinearMath/Quaternion.h>
#include <tf2/exceptions.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <tf2_ros/buffer.h>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2_ros/transform_listener.h>

#include "vault_sensors/fix_odom_frame_node.hpp"

using std::placeholders::_1;

FixOdomFrameNode::FixOdomFrameNode() : rclcpp::Node("fix_odom_frame_node") {

  this->declare_parameter<std::string>("frame_id", "base_link");
  this->get_parameter("frame_id", this->frame_id);

  this->declare_parameter<std::string>("odom_frame", "odom");
  this->get_parameter("odom_frame", this->odom_frame);

  this->declare_parameter<bool>("publish_tf", false);
  this->get_parameter("publish_tf", this->publish_tf);

  this->tf_buffer = std::make_unique<tf2_ros::Buffer>(this->get_clock());
  this->transform_listener =
      std::make_shared<tf2_ros::TransformListener>(*this->tf_buffer);
  this->tf_broadcaster = std::make_unique<tf2_ros::TransformBroadcaster>(*this);

  this->pub = this->create_publisher<nav_msgs::msg::Odometry>("odom_out", 200);
  this->sub = this->create_subscription<nav_msgs::msg::Odometry>(
      "odom_in", rclcpp::SensorDataQoS(),
      std::bind(&FixOdomFrameNode::callback, this, _1));
}

void FixOdomFrameNode::callback(const nav_msgs::msg::Odometry::SharedPtr msg) {

  geometry_msgs::msg::TransformStamped transform_stamped;
  geometry_msgs::msg::TransformStamped new_odom_transform;
  geometry_msgs::msg::PoseWithCovarianceStamped pose_stamped;

  try {
    transform_stamped = this->tf_buffer->lookupTransform(
        this->frame_id, msg->child_frame_id, tf2::TimePointZero);

    pose_stamped.header = msg->header;
    pose_stamped.pose = msg->pose;

    tf2::doTransform(pose_stamped, pose_stamped, transform_stamped);

    // new odom msg
    nav_msgs::msg::Odometry new_odom;

    new_odom.header.frame_id = this->odom_frame;
    new_odom.header.stamp = msg->header.stamp;
    new_odom.child_frame_id = this->frame_id;
    new_odom.pose = pose_stamped.pose;
    new_odom.twist = msg->twist;

    this->pub->publish(new_odom);

    // new odom tf
    if (this->publish_tf) {
      new_odom_transform.header = new_odom.header;
      new_odom_transform.child_frame_id = new_odom.child_frame_id;

      new_odom_transform.transform.translation.x =
          new_odom.pose.pose.position.x;
      new_odom_transform.transform.translation.y =
          new_odom.pose.pose.position.y;
      new_odom_transform.transform.translation.z =
          new_odom.pose.pose.position.z;

      new_odom_transform.transform.rotation.x =
          new_odom.pose.pose.orientation.x;
      new_odom_transform.transform.rotation.y =
          new_odom.pose.pose.orientation.y;
      new_odom_transform.transform.rotation.z =
          new_odom.pose.pose.orientation.z;
      new_odom_transform.transform.rotation.w =
          new_odom.pose.pose.orientation.w;
      this->tf_broadcaster->sendTransform(new_odom_transform);
    }

  } catch (tf2::TransformException &ex) {
    RCLCPP_WARN(this->get_logger(), "Could not transform %s to %s: %s",
                msg->child_frame_id.c_str(), this->frame_id.c_str(), ex.what());
  }
}

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<FixOdomFrameNode>());
  rclcpp::shutdown();
  return 0;
}