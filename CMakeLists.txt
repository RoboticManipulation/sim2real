cmake_minimum_required(VERSION 3.0.2)
project(cam2base)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  roscpp
  tf
  robot_state_publisher
  rviz
)

## Declare a catkin package
catkin_package(
  CATKIN_DEPENDS roscpp tf robot_state_publisher rviz
)

## Install launch files
install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

# Install Python scripts
catkin_install_python(PROGRAMS
  scripts/camera_info_republisher.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
