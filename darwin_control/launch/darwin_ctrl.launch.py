import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (AppendEnvironmentVariable, DeclareLaunchArgument, SetEnvironmentVariable,
                            IncludeLaunchDescription, SetLaunchConfiguration, RegisterEventHandler)
from launch.event_handlers import OnProcessExit
from launch.conditions import IfCondition
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from xacro import process_file
from nav2_common.launch import ReplaceString

ARGUMENTS = [
    DeclareLaunchArgument('world_name', default_value='empty.sdf', description='Name of the world to load. Match with map if using Nav2.'),
    DeclareLaunchArgument('ros_bridge', default_value='True', description='Run ROS bridge node.'),
    DeclareLaunchArgument('initial_pose_x', default_value='0.5', description='Initial x pose of rasbot in the simulation.'),
    DeclareLaunchArgument('initial_pose_y', default_value='0.0', description='Initial y pose of rasbot in the simulation.'),
    DeclareLaunchArgument('initial_pose_z', default_value='0.35', description='Initial z pose of rasbot in the simulation.'),
    DeclareLaunchArgument('initial_pose_yaw', default_value='0.0', description='Initial yaw pose of rasbot in the simulation.'),
    DeclareLaunchArgument('robot_description_topic', default_value='robot_description', description='Robot description topic.'),
    DeclareLaunchArgument('rsp_frequency', default_value='30.0', description='Robot State Publisher frequency.'),
    DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulation (Gazebo) clock if true'),
    DeclareLaunchArgument('entity', default_value='darwin', description='Name of the robot'),
]

# -------------------------- LAUNCH SCRIPT --------------------------------#

# 1. Load the robot descruption
def get_robot_description():
    pkg_darwin_ctrl = get_package_share_directory('darwin_control')
    robot_description_path = os.path.join(pkg_darwin_ctrl, 'urdf', 'darwin_ctrl.urdf.xacro')
    mappings = {}
    robot_description_config = process_file(robot_description_path, mappings=mappings)
    robot_desc = robot_description_config.toprettyxml(indent='  ')
    robot_desc = robot_desc.replace(
        'package://darwin_control/', f'file://{pkg_darwin_ctrl}/'
    )
    return robot_desc

#2. Generate launch description
def generate_launch_description():
    ld = LaunchDescription(ARGUMENTS)

    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_darwin_ctrl = get_package_share_directory('darwin_control')
    pkg_darwin_gz = get_package_share_directory('darwin_gazebo')
    gz_launch_path = PathJoinSubstitution([pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'])
    world_name = LaunchConfiguration('world_name')
    ros_bridge = LaunchConfiguration('ros_bridge')
    world_path = PathJoinSubstitution([pkg_darwin_gz,'worlds',world_name])
    controller_config_path = os.path.join(pkg_darwin_ctrl, 'config', 'nao_controller_manager.yaml')
    bridge_config_file_path = os.path.join(pkg_darwin_gz, 'config', 'bridge_config.yaml')

    ld.add_action(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch_path),
            launch_arguments={
                'gz_args': [world_path],
                'on_exit_shutdown': 'True'
            }.items(),
        ),
    )

    ld.add_action(
        Node(
                package='ros_gz_bridge',
                executable='parameter_bridge',
                arguments=['/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'],
                output='screen',
                namespace='andino_gz_sim',
                condition=IfCondition(ros_bridge),
            ),
    )

    use_sim_time = LaunchConfiguration('use_sim_time')
    rsp_frequency = LaunchConfiguration('rsp_frequency')

    ld.add_action(
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='both',
            parameters=[
                {
                    'use_sim_time': use_sim_time,
                    'publish_frequency':  rsp_frequency,
                    'robot_description': get_robot_description(),
                }
            ],
            remappings=[
                ('/tf', 'tf'),
                ('/tf_static', 'tf_static'),
            ],
        ),
    )

    entity = LaunchConfiguration('entity')
    initial_pose_x = LaunchConfiguration('initial_pose_x')
    initial_pose_y = LaunchConfiguration('initial_pose_y')
    initial_pose_z = LaunchConfiguration('initial_pose_z')
    initial_pose_yaw = LaunchConfiguration('initial_pose_yaw')
    robot_description_topic = LaunchConfiguration('robot_description_topic')
    nao_gz_spawn = Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', entity,
                '-topic', robot_description_topic,
                '-x', initial_pose_x,
                '-y', initial_pose_y,
                '-z', initial_pose_z,
                '-R', '0',
                '-P', '0',
                '-Y', initial_pose_yaw,
            ],
            output='screen',
        )
    ld.add_action(
        nao_gz_spawn
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
    )

    nao_controller_spawner_head = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller_head',
                   '--param-file',
                   controller_config_path,
        ],
    )

    nao_controller_spawner_right_leg = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller_right_leg',
                   '--param-file',
                   controller_config_path,
        ],
    )

    nao_controller_spawner_right_arm = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller_right_arm',
                   '--param-file',
                   controller_config_path,
        ],
    )

    nao_controller_spawner_left_leg = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller_left_leg',
                   '--param-file',
                   controller_config_path,
        ],
    )

    nao_controller_spawner_left_arm = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller_left_arm',
                   '--param-file',
                   controller_config_path,
        ],
    )

    ld.add_action(RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=nao_gz_spawn,
                on_exit=[joint_state_broadcaster_spawner],
            )
        )
    )
    ld.add_action(
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[nao_controller_spawner_head],
            )
        )
    )
    ld.add_action(
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[nao_controller_spawner_left_arm],
            )
        )
    )
    ld.add_action(
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[nao_controller_spawner_left_leg],
            )
        )
    )
    ld.add_action(
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[nao_controller_spawner_right_arm],
            )
        )
    )
    ld.add_action(
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[nao_controller_spawner_right_leg],
            )
        )
    )
    # bridge_config = ReplaceString(
    #     source_file=bridge_config_file_path,
    #     replacements={'<entity>': entity},
    # )

    # ld.add_action(
    #     Node(
    #         package='ros_gz_bridge',
    #         executable='parameter_bridge',
    #         output='screen',
    #         parameters=[{
    #             'config_file': bridge_config
    #         }],
    #     )
    # )

    return ld