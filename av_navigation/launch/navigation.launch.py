import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    pkg_nav2_dir = get_package_share_directory('nav2_bringup')
    pkg_av_navigation_dir = get_package_share_directory('av_navigation')

    # Declare launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='False',
        description='Use simulation time'
    )
    
    declare_autostart = DeclareLaunchArgument(
        'autostart',
        default_value='True',
        description='Automatically start lifecycle nodes'
    )
    
    declare_map = DeclareLaunchArgument(
        'map',
        default_value='gdc_3n',
        description='Map name (without .yaml extension)'
    )

    # Get launch configurations
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    map_name = LaunchConfiguration('map')

    # Print map name
    print(f"Map name: {map_name}")

    # Resolve map and config from the installed package share dir (works in any
    # workspace, including airfield containers). Requires setup.py to install
    # the maps/ and config/ data files.
    map_yaml_file = PathJoinSubstitution([
        os.path.join(pkg_av_navigation_dir, 'maps'),
        [map_name, '.yaml']
    ])

    nav2_config_file = os.path.join(pkg_av_navigation_dir, 'config', 'nav2.yaml')

    nav2_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2_dir, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'autostart': autostart,
            'map': map_yaml_file,
            'params_file': nav2_config_file,
            'package_path': pkg_av_navigation_dir, 
        }.items()
    )

    # Twist to Ackermann converter node
    # Converts Nav2's cmd_vel output to ackermann_curvature_drive for VESC driver
    twist_to_ackermann_node = Node(
        package='av_navigation',
        executable='twist_to_ackermann',
        name='twist_to_ackermann_converter',
        output='screen',
        parameters=[{
            'input_topic': 'cmd_vel',  # Nav2 controller output
            'output_topic': '/ackermann_curvature_drive',  # VESC driver input
            'wheelbase': 0.324,  # meters, should match vesc.lua config
            'max_curvature': 1.25,  # 1/meters (inverse of minimum turning radius ~0.8m)
        }]
    )

    ld = LaunchDescription()

    # Add launch argument declarations
    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_autostart)
    ld.add_action(declare_map)
    
    # Add nodes and other launch actions
    ld.add_action(nav2_launch_cmd)
    ld.add_action(twist_to_ackermann_node)

    return ld