cmake_minimum_required(VERSION 3.0.2)
project(cucr_worlds_hospital)

add_compile_options(-std=c++11)

find_package(gazebo_ros_link_attacher QUIET)

find_package(catkin REQUIRED
  COMPONENTS 
    roscpp
    moveit_core
    moveit_ros_planning
    moveit_ros_planning_interface
    gazebo_ros
)


find_package(Boost REQUIRED system filesystem date_time thread)

catkin_package(
    CATKIN_DEPENDS
)

include_directories(SYSTEM ${Boost_INCLUDE_DIR})
include_directories(${catkin_INCLUDE_DIRS})
link_directories(${catkin_LIBRARY_DIRS})

install(DIRECTORY models worlds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
