cmake_minimum_required(VERSION 3.5)
project(vault_visualization)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(image_transport REQUIRED)
find_package(pluginlib REQUIRED)

install(
  DIRECTORY launch rviz
  DESTINATION share/${PROJECT_NAME}
)

add_executable(republish_node src/republish_node.cpp)
target_link_libraries(republish_node)
ament_target_dependencies(republish_node
  rclcpp image_transport pluginlib)
install(
  TARGETS republish_node
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

ament_package()