'''
Interest marker node.
Subscribes to interestingness/info.
Publishes to interestingness/marker.
'''

import os
import sys

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from rcl_interfaces.msg import ParameterDescriptor

from interfaces.msg import InterestInfo
from visualization_msgs.msg import Marker 

# Need these paths for import to work correctly
int_ros_dir = ('/root/ros2_ws/src/interestingness_ros')
int_dir = ('/root/ros2_ws/src/interestingness_ros/interestingness')
sys.path.append(int_ros_dir)
sys.path.append(int_dir)
from interestingness.online import level_height


class InterestMarker(Node):

    def __init__(self):
        super().__init__("interestmarker_node") 
        self.declare_parameter('min-level', 0.1, ParameterDescriptor(description='minimum interest level to show')) # removed relative as param is local to this node
        self.min_level = self.get_parameter('min-level').value

        self.publisher = self.create_publisher(Marker, "interestmarker/marker", 10)
        self.subscriber = self.create_subscription(InterestInfo, "/interestingness/info", self.info_callback, 10)

    def info_callback(self, msg):
        level = level_height(msg.level)
        if level < self.min_level:
            self.get_logger().info(f'Skip interest with level: {level}')
            return
        marker = Marker()
        # marker.id = msg.header.seq # header does not contain seq
        marker.header = msg.header
        marker.type = marker.SPHERE
        marker.action = marker.ADD        

        marker.color.a = level
        marker.color.r, marker.color.g, marker.color.b = 1., 0., 0.
        marker.scale.x, marker.scale.y, marker.scale.z = [4*level]*3

        marker.pose.orientation.w = 1.
        marker.pose.position.z = 3.
        marker.lifetime = Duration(seconds=9999,nanoseconds=9999).to_msg()

        self.publisher.publish(marker)
        self.get_logger().warning(f'Sent interests with level: {level}')


def main(args=None):
    rclpy.init(args=args)
    node = InterestMarker()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()