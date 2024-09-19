#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image

class ImageAndCameraInfoRepublisher(Node):
    def __init__(self):
        super().__init__('image_and_camera_info_republisher')
        
        # Declare parameters
        self.declare_parameter('new_frame_id', 'camera_color_optical_frame_simulation')
        self.declare_parameter('camera_info_input_topic', '/camera/color/camera_info')
        self.declare_parameter('camera_info_output_topic', '/camera/color/camera_info_simulation')
        self.declare_parameter('image_input_topic', '/camera/color/image_raw')
        self.declare_parameter('image_output_topic', '/camera/color/image_raw_simulation')
        
        # Get parameters
        self.new_frame_id = self.get_parameter('new_frame_id').value
        self.camera_info_input_topic = self.get_parameter('camera_info_input_topic').value
        self.camera_info_output_topic = self.get_parameter('camera_info_output_topic').value
        self.image_input_topic = self.get_parameter('image_input_topic').value
        self.image_output_topic = self.get_parameter('image_output_topic').value
        
        # Create subscribers
        self.camera_info_subscriber = self.create_subscription(
            CameraInfo,
            self.camera_info_input_topic,
            self.camera_info_callback,
            10)
        self.image_subscriber = self.create_subscription(
            Image,
            self.image_input_topic,
            self.image_callback,
            10)
        
        # Create publishers
        self.camera_info_publisher = self.create_publisher(
            CameraInfo,
            self.camera_info_output_topic,
            10)
        self.image_publisher = self.create_publisher(
            Image,
            self.image_output_topic,
            10)
        
    def camera_info_callback(self, camera_info):
        # Modify the frame_id
        camera_info.header.frame_id = self.new_frame_id
        
        # Publish the modified CameraInfo
        self.camera_info_publisher.publish(camera_info)
        
    def image_callback(self, image):
        # Modify the frame_id
        image.header.frame_id = self.new_frame_id
        
        # Publish the modified Image
        self.image_publisher.publish(image)

def main(args=None):
    rclpy.init(args=args)
    republisher = ImageAndCameraInfoRepublisher()
    rclpy.spin(republisher)
    republisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()