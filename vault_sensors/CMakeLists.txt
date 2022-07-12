cmake_minimum_required(VERSION 3.5)
project(vault_sensors)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)

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

install(
  DIRECTORY config launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()