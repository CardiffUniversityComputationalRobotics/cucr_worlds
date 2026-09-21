# CUCR Worlds

Gazebo simulation worlds used by CUCR, packaged for **ROS 2 Jazzy** and **Gazebo Sim Harmonic (gz-sim 8)**.

Each package ships a world, the models it needs, an occupancy map for offline
navigation where one exists, and a `full.launch.py` that starts Gazebo on that
world. The launch files bring up the simulation only — no robot is spawned.

## Requirements

- ROS 2 Jazzy
- Gazebo Sim Harmonic (`gz-sim` 8)
- `ros_gz_sim` (`sudo apt install ros-jazzy-ros-gz-sim`)

## Packages

| Package | World file(s) | Map |
| --- | --- | --- |
| `cucr_worlds_small_house` | `small_house.world` | `small_house.yaml` |
| `cucr_worlds_small_warehouse` | `small_warehouse.world`, `no_roof_small_warehouse.world` | `small_warehouse.yaml` |
| `cucr_worlds_bookstore` | `bookstore.world` | `map.yaml`, `map.bt`, `map.ot` |
| `cucr_worlds_hospital` | `hospital.world`, `empty_default.world` | `hospital.yaml`, `hospital.bt`, `hospital.ot` |
| `cucr_worlds_museum` | `museum.world`, `empty_default.world` | `map.yaml`, `map.bt` |
| `cucr_worlds_house_museum` | `house_museum.world`, `empty_default.world` | `map.yaml` |
| `cucr_worlds_office` | `office.world` | `office.yaml` |

`.pgm`/`.yaml` are 2D occupancy grids for Nav2; `.bt`/`.ot` are OctoMap files.

## Build

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/CardiffUniversityComputationalRobotics/cucr_worlds.git

cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Sourcing the workspace is what makes the worlds runnable: each package installs
an environment hook that prepends its `models/` and `worlds/` directories to
`GZ_SIM_RESOURCE_PATH`, so Gazebo can resolve the `model://` URIs inside the
world files. Without sourcing, Gazebo starts with an empty scene and logs
`Unable to find uri[model://...]`.

## Running the small house

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 launch cucr_worlds_small_house full.launch.py
```

Gazebo opens on `small_house.world`, already unpaused (`-r`).

Headless, for CI or when you only need the physics server:

```bash
ros2 launch cucr_worlds_small_house full.launch.py use_gazebo_gui:=False
```

To load a different world file through the same launch file:

```bash
ros2 launch cucr_worlds_small_house full.launch.py \
  world:=$(ros2 pkg prefix --share cucr_worlds_small_house)/worlds/small_house.world
```

Or bypass ROS entirely once the workspace is sourced — the resource hook is set
either way:

```bash
gz sim -r $(ros2 pkg prefix --share cucr_worlds_small_house)/worlds/small_house.world
```

Check that it came up:

```bash
gz topic -l | head            # /clock, /stats, /world/default/...
gz model --list               # models present in the scene
```

The matching Nav2 map lives at
`$(ros2 pkg prefix --share cucr_worlds_small_house)/maps/small_house.yaml`.

### Launch arguments

Every package exposes the same two arguments:

| Argument | Default | Meaning |
| --- | --- | --- |
| `world` | the package's own world file | Full path to the world file to load |
| `use_gazebo_gui` | `True` | `False` runs the server headless (`gz sim -s -r`) |

## Running the other worlds

Same pattern, swap the package name:

```bash
ros2 launch cucr_worlds_small_warehouse full.launch.py
ros2 launch cucr_worlds_bookstore full.launch.py
ros2 launch cucr_worlds_hospital full.launch.py
ros2 launch cucr_worlds_museum full.launch.py
ros2 launch cucr_worlds_house_museum full.launch.py
ros2 launch cucr_worlds_office full.launch.py
```

Packages with a second world file load it through the `world` argument:

```bash
ros2 launch cucr_worlds_small_warehouse full.launch.py \
  world:=$(ros2 pkg prefix --share cucr_worlds_small_warehouse)/worlds/no_roof_small_warehouse.world
```

## Spawning a robot

These packages deliberately contain no robot. Start a world, then spawn a model
into the running simulation with `ros_gz_sim`:

```bash
ros2 launch cucr_worlds_small_house full.launch.py &

ros2 run ros_gz_sim create -world default -file /path/to/robot.sdf -name my_robot -z 0.1
```

Bridge the topics you need with `ros_gz_bridge` (`/clock`, `/cmd_vel`, `/scan`, …);
`ros_gz_sim` does not bridge anything on its own.

## Credits

- `cucr_worlds_museum`, `cucr_worlds_house_museum` — CUCR, based on the National
  Museum Cardiff.
- `cucr_worlds_hospital`, `cucr_worlds_bookstore`, `cucr_worlds_small_house`,
  `cucr_worlds_small_warehouse` — [aws-robotics](https://github.com/aws-robotics)
  RoboMaker world assets.
- `cucr_worlds_office` — ServiceSim office environment.
