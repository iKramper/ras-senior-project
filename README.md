# ROBOTIS's DARWIN-MINI in ROS 2

Simulation of the ROBOTIS DARWIN-MINI in ROS 2 Jazzy and Gazebo Harmonic. Currently, the robot can be visualized in RViz2, spawned in Gazebo and be sent to a home position using ROS 2 Control action clients. ROS 2 Gazebo Bridge (abbreviated as ROS 2 GZ Bridge in this documentation) is also enabled and working.

## Full Repository Structure

```
.
├── darwin_control
│   ├── CMakeLists.txt
│   ├── config
│   │   └── darwin_controller_manager.yaml
│   ├── launch
│   │   └── darwin_ctrl.launch.py
│   ├── package.xml
│   ├── src
│   │   └── home_position.cpp
│   └── urdf
│       └── darwin_ctrl.urdf.xacro
├── darwin_description
│   ├── CMakeLists.txt
│   ├── docs
│   │   └── optimal_origins.txt
│   ├── launch
│   │   └── display_darwin.launch.py
│   ├── meshes
│   │   ├── DMB-B02(W).stl
│   │   ├── DMF-B01(W).stl
│   │   ├── DMF-B03(W).stl
│   │   ├── DMF-B04(W).stl
│   │   ├── DMF-B05(W).stl
│   │   ├── DMF-B06(W).stl
│   │   ├── DMF-B07(GR).stl
│   │   ├── DMF-F01(W).stl
│   │   ├── SPD-3B3(W).stl
│   │   ├── SPD-3B5(W).stl
│   │   ├── SPD-3B7(W).stl
│   │   ├── SPD-4B5(W).stl
│   │   ├── SPD-7V4(W).stl
│   │   ├── SPL-2B2(W).stl
│   │   ├── SPO-5(GR).stl
│   │   ├── SPU-5(W).stl
│   │   └── XL-320D.stl
│   ├── package.xml
│   └── urdf
│       ├── arm.urdf.xacro
│       ├── base.urdf.xacro
│       ├── body.urdf.xacro
│       ├── common.urdf.xacro
│       ├── darwin.urdf.xacro
│       ├── hand.urdf.xacro
│       ├── leg.urdf.xacro
│       ├── materials.urdf.xacro
│       └── servo.urdf.xacro
├── darwin_gazebo
│   ├── CMakeLists.txt
│   ├── config
│   │   └── bridge_config.yaml
│   ├── launch
│   │   └── darwin_gz.launch.py
│   ├── package.xml
│   ├── urdf
│   │   └── darwin_gz.urdf.xacro
│   └── worlds
│       └── empty.sdf
└── README.md
```

## Requisites

- ROS2 Jazzy
- Gazebo Harmonic
- `ros-jazzy-ros-gz-bridge`
- `ros-jazzy-xacro`
- `ros-jazzy-robot-state-publisher`
- `ros-jazzy-ros2-control`
- `ros-jazzy-ros2-controllers`
- `ros-jazzy-gz-ros2-control`

> It is highly recommended to use some Linux distro as your OS. This documentation assumes that you are using a Linux distro. Tutorials for Windows may be added in the future.

## Package Overview

### darwin_description

```
darwin/src/darwin_description/
├── CMakeLists.txt
├── docs
│   └── home_joint_values.md
├── launch
│   └── display_darwin.launch.py
├── meshes
├── package.xml
└── urdf
```

**darwin_description** package includes:

- Meshes and urdf files of the robot
- Launch file to display DARWIN in RViz2
- Information about predefined joint configurations in `docs/`.

### darwin_gazebo

```
darwin/src/gazebo/
├── CMakeLists.txt
├── config
│   └── bridge_config.yaml
├── launch
│   └── darwin_gz.launch.py
├── package.xml
├── urdf
│   └── darwin_gz.urdf.xacro
└── worlds
    └── empty.sdf
```

**darwin_gazebo** package contains:

- The configuration file for ROS 2 GZ Bridge
- Launch file to spawn DARWIN in Gazebo
- URDF file that includes the necessary plugins to enable ROS 2 GZ communication
- Empty Gazebo's world for simulation

### darwin_control

```
├── CMakeLists.txt
├── config
│   └── darwin_controller_manager.yaml
├── launch
│   └── darwin_ctrl.launch.py
├── package.xml
├── src
│   └── home_position.cpp
└── urdf
    └── darwin_ctrl.urdf.xacro
```

**darwin_control** package has:

- The configuration file for ROS 2 Control
- Launch file to spawn DARWIN in Gazebo with a predefined pose
- Node `home_position` that drives DARWIN to the HOME position
- URDF file that defines the controllable joints and their parameters

## Getting Started

### 1. Create a workspace and a source folder for the project

```bash
mkdir -p darwin/src
cd darwin/src
```

### 2. Clone and build

```bash
git clone https://github.com/iKramper/ros-2-robotis-darwin-mini.git .
cd ..
colcon build
source install/setup.bash
cd src
```

### 3. Launch simulation (Gazebo)

```bash
ros2 launch darwin_control darwin_ctrl.launch.py
```

This launches:

- ROS 2 GZ Bridge
- Gazebo Harmonic simulation
- ros2_control controllers

### 4. Send robot to HOME position

Open another terminal and, within the folder of the workspace that you have created, execute:

```bash
source install/setup.bash
cd src
ros2 run darwin_control home_position
```

## Usage

> A _sourced terminal_ means a terminal where you have run the command `source install/setup.bash` inside your _workspace_ folder and then moved to the `src` directory. All following instructions assume that you are working in a sourced terminal.

### Verify controllers

Before sending any commands (via action calls, for example) it is highly recommended to check whether the controllers are active. Controller activation can sometimes fail during launch.

##### Check controller status:

```bash
ros2 control list_controllers
```

#### Expected output:

```bash
joint_trajectory_controller_general joint_trajectory_controller/JointTrajectoryController  active
joint_state_broadcaster             joint_state_broadcaster/JointStateBroadcaster          active
```

All controllers should show `active status. If any controller shows `inactive`or`unconfigured, see the [Troubleshooting](#troubleshooting) section below.

### Send DARWIN to a given position

DARWIN can be driven to any position in Gazebo via action calls:

```bash
ros2 action send_goal --feedback \
/joint_trajectory_controller_general/follow_joint_trajectory \
control_msgs/action/FollowJointTrajectory \
"{
  trajectory: {
    joint_names: [
      'neck_joint',
      'r_hip_joint',
      'r_thigh_joint',
      'r_knee_joint',
      'r_ankle_joint',
      'r_foot_joint',
      'r_shoulder_joint',
      'r_biceps_joint',
      'r_elbow_joint',
      'l_hip_joint',
      'l_thigh_joint',
      'l_knee_joint',
      'l_ankle_joint',
      'l_foot_joint',
      'l_shoulder_joint',
      'l_biceps_joint',
      'l_elbow_joint'
    ],
    points: [
      {
        positions: [2.66, 5.23, 0.00, 1.78, 0.00, 0.00, 2.27, 1.54, 3.31, 0.00, 0.00, 1.84, 0.00, 5.23, 2.60, 3.76, 1.75],
        time_from_start: {
          sec: 5,
          nanosec: 0
        }
      }
    ]
  }
}"
```

Just change the numeric values of `positions` for each corresponding joint to construct the desired pose. All joints are revolute and their range of movement is between 0.00 rad (0°) and 5.266 rad (300°). You can also change `time_from_start` if you want a faster or slower movement.

If you wish to move just one joint or a specified set of joints you can also run something like this:

```bash
ros2 action send_goal --feedback \
/joint_trajectory_controller_general/follow_joint_trajectory \
control_msgs/action/FollowJointTrajectory \
"{
  trajectory: {
    joint_names: [
      'r_shoulder_joint',
      'r_biceps_joint',
      'r_elbow_joint'
    ],
    points: [
      {
        positions: [2.27, 1.54, 3.31],
        time_from_start: {
          sec: 1,
          nanosec: 0
        }
      }
    ]
  }
}"
```

It is important that, for natural movements, the values for `positions` are between the ranges provided in `movement_ranges.md`, which can be found at `docs/` folder of `darwin_control`.

### Visualize DARWIN in RViz2

```bash
ros2 launch darwin_description display_darwin.launch.py
```

### Spawn DARWIN in Gazebo (without controllers)

```bash
ros2 launch darwin_gazebo darwin_gz.launch.py
```

ROS 2 GZ Bridge will be enabled.

## Troubleshooting

### Controllers not activating automatically?

If `ros2 control list_controllers shows any controller as inactive or unconfigured, you can activate them manually:

```bash
ros2 control switch_controllers \
  --activate joint_state_broadcaster \
  --activate right_arm_controller \
  --activate left_arm_controller \
  --activate head_controller
```

Verify all controllers are now active:

```bash
ros2 control list_controllers
```

All controllers should show `active` status.

### The controllers never activate automatically?

If you notice that the controllers never activate automatically and you constantly have to activate them manually, try to run the Gazebo simulation as soon as it launches. The controllers try always to initialize as soon as Gazebo opens but if the simulation is not running, they will fail.

### Robot not showing in Gazebo simulation?

If some parts of the DARWIN robot do not appear or the robot does not appear at all you are probably running `darwin_ctrl.launch.py` from your workspace root instead of the `src` directory.

## Acknowledgements

This project includes resources from:

- https://github.com/japonophile/darwin
  - Resources: `meshes` and `urdf` folders and their files
  - License: MIT
  - Copyright © 2016 Antoine Choppin

The content of those directories was used to display DARWIN in RViz2, and later the files were modified in `darwin_gazebo` and `darwin_description` packages by adding plugins for Gazebo and ROS 2 Controllers.

## Future work

- The collisions of the robot do not appear to work. Some trajectories may cross the body of the robot. The original URDF files could be reviewed.
- Future work may include poses for the robot or even implementing a walking algorithm, all of this via action calls or proper tools
