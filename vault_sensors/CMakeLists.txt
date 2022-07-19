cmake_minimum_required(VERSION 3.5)
project(vault_sensors)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)

INCLUDE_DIRECTORIES(
  include
)

add_executable(fix_imu_frame_node src/fix_imu_frame_node.cpp)
target_link_libraries(fix_imu_frame_node)
ament_target_dependencies(fix_imu_frame_node rclcpp sensor_msgs)
install(TARGETS
  fix_imu_frame_node
  DESTINATION lib/${PROJECT_NAME}
)

add_executable(fix_odom_frame_node src/fix_odom_frame_node.cpp)
target_link_libraries(fix_odom_frame_node)
ament_target_dependencies(fix_odom_frame_node
  rclcpp nav_msgs
  geometry_msgs
  tf2
  tf2_ros
  tf2_geometry_msgs)
install(TARGETS
  fix_odom_frame_node
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY config launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()