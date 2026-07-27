# ROBOTIS's DARWIN-MINI in ROS 2

Simulation of the ROBOTIS DARWIN-MINI in ROS 2 Jazzy and Gazebo Harmonic. Currently, the robot can be visualized in RViz2, spawned in Gazebo and be sent to a home position using ROS 2 Control action clients. ROS 2-GZ Bridge is also enabled and working.

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

---

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

---

## Getting Started

### 1. Create a workspace for the project

```bash
mkdir darwin
cd darwin
```

### 2. Clone and build

```bash
git clone https://github.com/iKramper/ros-2-robotis-darwin-mini.git .
colcon build
source install/setup.bash
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

Open another terminal and, within the workspace that you have created, execute:

```bash
source install/setup.bash
ros2 run darwin_control home_position
```

---

## Usage

### Send
