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

    # Construct map file path using source directory
    home_dir = os.path.expanduser('~')
    map_yaml_file = PathJoinSubstitution([
        os.path.join(home_dir, 'roboracer_ws', 'src', 'av_navigation', 'av_navigation', 'maps'),
        [map_name, '.yaml']
    ])

    # Construct nav2 config file path using source directory
    nav2_config_file = os.path.join(home_dir, 'roboracer_ws', 'src', 'av_navigation', 'av_navigation', 'config', 'nav2.yaml')

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

    ld = LaunchDescription()

    # Add launch argument declarations
    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_autostart)
    ld.add_action(declare_map)
    
    # Add nodes and other launch actions
    ld.add_action(nav2_launch_cmd)

    return ld