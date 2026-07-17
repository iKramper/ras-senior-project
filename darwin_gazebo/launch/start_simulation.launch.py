#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -------------------------- LAUNCH DEPENDENCIES -------------------------
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.conditions import IfCondition

# ----------------------------- LAUNCH SCRIPT ----------------------------
def generate_launch_description():
    
    # Launch arguments:
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Use simulation (Gazebo) clock'
    )
    use_sim_time = LaunchConfiguration('use_sim_time')

    launch_gui_arg = DeclareLaunchArgument(
        'launch_gui', default_value='true',
        description='Launch the PropArm GUI interface'
    )
    launch_gui = LaunchConfiguration('launch_gui')

    gui_delay_arg = DeclareLaunchArgument(
        'gui_delay', default_value='8.0',
        description='Delay before launching GUI (seconds)'
    )

    # Find your packages:
    pkg_gz   = FindPackageShare("darwin_gazebo")
    pkg_desc = FindPackageShare("darwin_description")

    # Launch files:
    start_world    = PathJoinSubstitution([pkg_gz,   "launch", "start_world.launch.py"])
    # spawn_models     = PathJoinSubstitution([pkg_gz,   "launch", "spawn_models.launch.py"])
    publish_urdf       = PathJoinSubstitution([pkg_desc, "launch", "publish_urdf.launch.py"])
    spawn_darwin     = PathJoinSubstitution([pkg_gz,   "launch", "spawn_darwin.launch.py"])

    return LaunchDescription([
        use_sim_time_arg,
        launch_gui_arg,
        gui_delay_arg,

        # 1. Start Gazebo:
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(start_world ),
            launch_arguments={'use_sim_time': use_sim_time}.items()
        ),
        
        # 2. Publish URDF:
        TimerAction(
            period=3.0,
            actions=[ IncludeLaunchDescription(
                PythonLaunchDescriptionSource(publish_urdf),
                launch_arguments={'use_sim_time': use_sim_time}.items()
            ) ]
        ),

        # # 3. Spawn the models in Gazebo:
        # TimerAction(
        #     period=5.0,
        #     actions=[ IncludeLaunchDescription(
        #         PythonLaunchDescriptionSource(spawn_models),
        #         launch_arguments={'use_sim_time': use_sim_time}.items()
        #     ) ]
        # ),

        # 3. Spawn the robot in Gazebo:
        TimerAction(
            period=7.0,
            actions=[ IncludeLaunchDescription(
                PythonLaunchDescriptionSource(spawn_darwin),
                launch_arguments={'use_sim_time': use_sim_time}.items()
            ) ]
        ),
    ])