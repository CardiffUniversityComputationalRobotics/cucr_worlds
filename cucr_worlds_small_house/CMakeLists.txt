cmake_minimum_required(VERSION 3.0.2)
project(cucr_worlds_small_house)

find_package(catkin REQUIRED)

find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
)

catkin_package(
)

install(DIRECTORY models worlds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)