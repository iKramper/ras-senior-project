cmake_minimum_required(VERSION 3.8)
project(darwin_control)

# Set C++ standard:
if(NOT CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 17)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(control_msgs REQUIRED)
find_package(trajectory_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(rclcpp_components REQUIRED)

add_library(home_position_component SHARED
  src/home_position.cpp)
target_include_directories(home_position_component PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_definitions(home_position_component
  PRIVATE "DARWIN_CONTROL_BUILDING_DLL")
ament_target_dependencies(home_position_component
  "control_msgs"
  "trajectory_msgs"
  "rclcpp"
  "rclcpp_action"
  "rclcpp_components")
rclcpp_components_register_node(home_position_component PLUGIN "darwin_control::HomePosition" EXECUTABLE home_position)
install(TARGETS
  home_position_component
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)

install(DIRECTORY config launch src urdf
    DESTINATION share/${PROJECT_NAME} 
)

ament_package()
