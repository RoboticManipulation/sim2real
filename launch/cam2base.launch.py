import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node

def generate_launch_description():
    ur_description_path = get_package_share_directory('ur_description')
    urdf_file = os.path.join(ur_description_path, 'urdf', 'ur.urdf.xacro')

    # Define arguments for the xacro file
    xacro_args = {
        'name': 'ur',
        'ur_type': 'ur5',
        'use_fake_hardware': 'false',
        'sim_gazebo': 'false',
        'sim_ignition': 'false',
        'headless_mode': 'false',
    }

    xacro_command = Command([
        'xacro ', urdf_file, ' '] + 
        [f"{k}:={v} " for k, v in xacro_args.items()]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'urdf_file',
            default_value=urdf_file,
            description='URDF file for UR robot'
        ),

        # Debug: Print the xacro command
        ExecuteProcess(
            cmd=['echo', 'XACRO command:', xacro_command],
            output='screen'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': xacro_command}]
        ),

        # ... rest of your nodes ...

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher',
            arguments=['0.0', '0.0', '0.0', '-1.57', '0.0', '0.0', 'base_link', 'base_link_simulation']
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher2',
            arguments=['-0.256044', '0.433903', '1.0709928', '-3.11832', '3.13685', '0.0328435', 'base_link_simulation', 'camera_color_optical_frame']
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher3',
            arguments=['-0.256044', '0.433903', '1.0709928', '-3.11832', '3.13685', '0.0328435', 'base_link', 'camera_color_optical_frame_simulation']
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher4',
            arguments=['0', '0.1', '0.1', '0', '0', '0.785398', 'tool0', 'dummy']
        ),

        # Add your camera_info_republisher node here if needed
        #Node(
        #    package='sim2real',
        #    executable='camera_info_republisher',
        #    name='camera_info_republisher',
        #)
    ])