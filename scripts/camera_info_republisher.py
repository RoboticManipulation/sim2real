#!/usr/bin/env python

import rospy
from sensor_msgs.msg import CameraInfo, Image

class ImageAndCameraInfoRepublisher:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('image_and_camera_info_republisher', anonymous=True)
        
        # Get parameters
        self.new_frame_id = rospy.get_param('~new_frame_id', 'camera_color_optical_frame_simulation')
        self.camera_info_input_topic = rospy.get_param('~camera_info_input_topic', '/camera/color/camera_info')
        self.camera_info_output_topic = rospy.get_param('~camera_info_output_topic', '/camera/color/camera_info_simulation')
        self.image_input_topic = rospy.get_param('~image_input_topic', '/camera/color/image_raw')
        self.image_output_topic = rospy.get_param('~image_output_topic', '/camera/color/image_raw_simulation')
        
        # Create subscribers
        self.camera_info_subscriber = rospy.Subscriber(self.camera_info_input_topic, CameraInfo, self.camera_info_callback)
        self.image_subscriber = rospy.Subscriber(self.image_input_topic, Image, self.image_callback)
        
        # Create publishers
        self.camera_info_publisher = rospy.Publisher(self.camera_info_output_topic, CameraInfo, queue_size=10)
        self.image_publisher = rospy.Publisher(self.image_output_topic, Image, queue_size=10)
        
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

if __name__ == '__main__':
    try:
        republisher = ImageAndCameraInfoRepublisher()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

