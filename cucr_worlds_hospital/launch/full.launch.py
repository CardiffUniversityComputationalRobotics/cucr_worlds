import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    scene = "hospital"

    # ! PACKAGES DIR
    ros_gz_sim_dir = FindPackageShare(package="ros_gz_sim").find("ros_gz_sim")
    cucr_worlds_dir = FindPackageShare(package="cucr_worlds_hospital").find(
        "cucr_worlds_hospital"
    )

    world_model_path = os.path.join(cucr_worlds_dir, "worlds", scene + ".world")

    # ! LAUNCH PARAMETERS
    world = LaunchConfiguration("world")
    use_gazebo_gui = LaunchConfiguration("use_gazebo_gui")

    declare_world_cmd = DeclareLaunchArgument(
        "world",
        default_value=world_model_path,
        description="Full path to the world file to load",
    )
    declare_simulator_cmd = DeclareLaunchArgument(
        "use_gazebo_gui",
        default_value="True",
        description="Whether to run the Gazebo Sim GUI",
    )

    world_str_path = [TextSubstitution(text="-r "), world]
    world_str_path_headless = [TextSubstitution(text="-s -r "), world]

    # ! Start Gazebo Sim
    start_gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_dir, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": world_str_path}.items(),
        condition=IfCondition(use_gazebo_gui),
    )

    start_gazebo_headless_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_dir, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": world_str_path_headless}.items(),
        condition=UnlessCondition(use_gazebo_gui),
    )

    ld = LaunchDescription()

    ld.add_action(declare_world_cmd)
    ld.add_action(declare_simulator_cmd)

    ld.add_action(start_gazebo_cmd)
    ld.add_action(start_gazebo_headless_cmd)

    return ld
