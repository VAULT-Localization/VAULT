
#define BOOST_BIND_NO_PLACEHOLDERS

#include <geometry_msgs/msg/transform_stamped.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <rclcpp/rclcpp.hpp>

#include <tf2/exceptions.h>
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

  this->tf_buffer_ = std::make_unique<tf2_ros::Buffer>(this->get_clock());
  this->transform_listener_ =
      std::make_shared<tf2_ros::TransformListener>(*this->tf_buffer_);
  this->tf_broadcaster_ =
      std::make_unique<tf2_ros::TransformBroadcaster>(*this);

  this->pub = this->create_publisher<nav_msgs::msg::Odometry>("odom_out", 10);
  this->sub = this->create_subscription<nav_msgs::msg::Odometry>(
      "odom_in", 10, std::bind(&FixOdomFrameNode::callback, this, _1));
}

void FixOdomFrameNode::callback(const nav_msgs::msg::Odometry::SharedPtr msg) {

  geometry_msgs::msg::TransformStamped transform_stamped;

  try {
    transform_stamped = tf_buffer_->lookupTransform(
        msg->child_frame_id, this->frame_id, tf2::TimePointZero);

    nav_msgs::msg::Odometry new_odom;

    new_odom.header.frame_id = this->odom_frame;
    new_odom.header.stamp = msg->header.stamp;

    new_odom.pose.pose.position.x =
        msg->pose.pose.position.x - transform_stamped.transform.translation.x;
    new_odom.pose.pose.position.y =
        msg->pose.pose.position.y - transform_stamped.transform.translation.y;
    new_odom.pose.pose.position.z =
        msg->pose.pose.position.z - transform_stamped.transform.translation.z;

    new_odom.pose.pose.orientation.x =
        msg->pose.pose.orientation.x - transform_stamped.transform.rotation.x;
    new_odom.pose.pose.orientation.y =
        msg->pose.pose.orientation.y - transform_stamped.transform.rotation.y;
    new_odom.pose.pose.orientation.z =
        msg->pose.pose.orientation.z - transform_stamped.transform.rotation.z;
    new_odom.pose.pose.orientation.w =
        msg->pose.pose.orientation.w - transform_stamped.transform.rotation.w;

    new_odom.pose.covariance = msg->pose.covariance;
    new_odom.twist = msg->twist;

    this->pub->publish(new_odom);
  } catch (tf2::TransformException &ex) {
    RCLCPP_WARN(this->get_logger(), "Could not transform %s to %s: %s",
                msg->child_frame_id.c_str(), this->frame_id.c_str(), ex.what());
    return;
  }
}

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<FixOdomFrameNode>());
  rclcpp::shutdown();
  return 0;
}