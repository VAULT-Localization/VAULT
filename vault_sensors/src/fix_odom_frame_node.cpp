
#define BOOST_BIND_NO_PLACEHOLDERS

#include <cmath>

#include <geometry_msgs/msg/transform_stamped.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <rclcpp/rclcpp.hpp>

#include <tf2/LinearMath/Quaternion.h>
#include <tf2/exceptions.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
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

  try {
    transform_stamped = tf_buffer->lookupTransform(
        this->frame_id, msg->child_frame_id, tf2::TimePointZero);

    // rotate
    tf2::Quaternion q_orig, q_rot, q_new;
    tf2::convert(msg->pose.pose.orientation, q_orig);
    tf2::convert(transform_stamped.transform.rotation, q_rot);
    q_new = q_rot.inverse() * q_orig;
    q_new.normalize();

    // new odom msg
    nav_msgs::msg::Odometry new_odom;

    new_odom.header.frame_id = this->odom_frame;
    new_odom.header.stamp = msg->header.stamp;
    new_odom.child_frame_id = this->frame_id;

    double roll, pitch, yaw;
    tf2::Matrix3x3 m(q_rot);
    m.getRPY(roll, pitch, yaw);

    new_odom.pose.pose.position.x =
        msg->pose.pose.position.x -
        ((transform_stamped.transform.translation.x * cos(yaw)) -
         (-transform_stamped.transform.translation.y * sin(yaw)));
    new_odom.pose.pose.position.y =
        msg->pose.pose.position.y -
        ((transform_stamped.transform.translation.x * sin(yaw)) +
         (-transform_stamped.transform.translation.y * cos(yaw)));
    new_odom.pose.pose.position.z =
        msg->pose.pose.position.z - transform_stamped.transform.translation.z;

    tf2::convert(q_new, new_odom.pose.pose.orientation);

    new_odom.pose.covariance = msg->pose.covariance;
    new_odom.twist = msg->twist;

    // new odom tf
    new_odom_transform.header = new_odom.header;
    new_odom_transform.child_frame_id = new_odom.child_frame_id;

    new_odom_transform.transform.translation.x = new_odom.pose.pose.position.x;
    new_odom_transform.transform.translation.y = new_odom.pose.pose.position.y;
    new_odom_transform.transform.translation.z = new_odom.pose.pose.position.z;

    new_odom_transform.transform.rotation.x = new_odom.pose.pose.orientation.x;
    new_odom_transform.transform.rotation.y = new_odom.pose.pose.orientation.y;
    new_odom_transform.transform.rotation.z = new_odom.pose.pose.orientation.z;
    new_odom_transform.transform.rotation.w = new_odom.pose.pose.orientation.w;

    // publish
    this->pub->publish(new_odom);
    this->tf_broadcaster->sendTransform(new_odom_transform);

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