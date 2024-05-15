import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    scene = "hospital"

    pkg_gazebo_ros = FindPackageShare(package="gazebo_ros").find("gazebo_ros")
    cucr_worlds_dir = FindPackageShare(package="cucr_worlds_hospital").find(
        "cucr_worlds_hospital"
    )

    world_model_path = os.path.join(cucr_worlds_dir, "worlds", scene + ".world")

    world = LaunchConfiguration("world")
    use_gazebo_gui = LaunchConfiguration("use_gazebo_gui")

    declare_world_cmd = DeclareLaunchArgument(
        "world",
        default_value=world_model_path,
        description="Full path to world model file to load",
    )
    declare_simulator_cmd = DeclareLaunchArgument(
        "use_gazebo_gui",
        default_value="True",
        description="Whether to execute gzclient)",
    )

    # Start Gazebo server
    start_gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, "launch", "gazebo.launch.py")
        ),
        launch_arguments={"world": world, "gui": use_gazebo_gui}.items(),
    )

    ld = LaunchDescription()

    ld.add_action(declare_world_cmd)
    ld.add_action(declare_simulator_cmd)

    ld.add_action(start_gazebo_server_cmd)

    return ld
