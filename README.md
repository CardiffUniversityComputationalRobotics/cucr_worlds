# CUCR worlds
Here you will find all the necessary information in order to build the worlds created and used by CUCR within one metapackage.

## Museum
This map was created by CUCR.
### Installation
Before installing any new package, update your installed packages:
```bash
cucr-get update
```
To install dependecies within ros:
```bash
cucr-get install ros-cucr_worlds_museum
```
To build the new packages in either case:
```bash
cucr-make
```
### Launch the full network
To start the simulation (Gazebo):
```bash
roslaunch cucr_worlds_museum full.launch
```
> Note: The full.launch is only the simulation space. It does not contain any type of robot.

## hospital
This map was created by aws-robotics (https://github.com/aws-robotics/aws-robomaker-hospital-world.git).
### Installation
Before installing any new package, update your installed packages:
```bash
cucr-get update
```
To install dependecies within ros:
```bash
cucr-get install ros-cucr_worlds_hospital
```
To build the new packages in either case:
```bash
cucr-make
```
### Launch the full network
To start the simulation (Gazebo):
```bash
roslaunch cucr_worlds_hospital full.launch
```
> Note: The full.launch is only the simulation space. It does not contain any type of robot.

