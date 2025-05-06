from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    package_name = 'assignment2'
    rosbag_path = os.path.join(FindPackageShare(package_name).find(package_name),
                                     'rosbag_cones', 'cones.db3')



    return LaunchDescription([
        Node(
            package=package_name,
            executable='pointcloud_classifier',
            output='screen'
        ),
        ExecuteProcess(
            cmd=['ros2', 'bag', 'play', rosbag_path],
            output='screen'
        )
    ])