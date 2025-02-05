from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get the package share directory
    pkg_share = get_package_share_directory('edo_sim')
    
    # Declare arguments
    # gui_arg = DeclareLaunchArgument(
    #     'gui',
    #     default_value='true',
    #     description='Flag to enable joint_state_publisher_gui'
    # )

    # Load the URDF file content
    urdf_file = os.path.join(pkg_share, 'robots', 'edo_sim.urdf')
    print("urdf_file: ", urdf_file)
    with open(urdf_file, 'r') as file:
        robot_description = file.read()

    # Define nodes
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'robot_description': robot_description}],
        # condition=UnlessCondition(LaunchConfiguration('gui'))
        output='screen',
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        name='robot_state_publisher',
        output='screen',
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(pkg_share, 'urdf.rviz')]
    )

    # joint_state_publisher_gui_node = Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     name='joint_state_publisher_gui',
    #     # condition=IfCondition(LaunchConfiguration('gui'))
    # )
    
    # Create and return launch description
    return LaunchDescription([
        # gui_arg,
        # joint_state_publisher_gui_node,
        # joint_state_publisher_node,
        robot_state_publisher_node,
        rviz_node
    ])