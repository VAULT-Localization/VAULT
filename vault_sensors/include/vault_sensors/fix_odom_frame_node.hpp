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

  std::shared_ptr<tf2_ros::TransformListener> transform_listener{nullptr};
  std::unique_ptr<tf2_ros::Buffer> tf_buffer;
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster;

  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr sub;
  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr pub;
};

#endif