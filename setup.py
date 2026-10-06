from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'av_navigation'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('av_navigation/launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('av_navigation/config/*.yaml')),
        (os.path.join('share', package_name, 'maps'), glob('av_navigation/maps/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Nathan Tsoi',
    maintainer_email='nathan@vertile.com',
    description='AV Navigation Stack',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'twist_to_ackermann = av_navigation.twist_to_ackermann:main',
        ],
    },
)
