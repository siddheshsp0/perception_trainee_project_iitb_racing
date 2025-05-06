from setuptools import find_packages, setup
from glob import glob


package_name = 'assignment2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/rosbag_cones', glob('rosbag_cones/*')),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Siddhesh',
    maintainer_email='siddheshsp0@gmail.com',
    description='Perception: Assignment2 - Reading and processing point cloud data',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pointcloud_classifier = assignment2.pointcloud_classifier:main'
        ],
    },
)
