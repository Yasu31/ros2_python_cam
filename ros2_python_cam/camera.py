import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

class CameraPublisher(Node):
    def __init__(self):
        super().__init__("camera_publisher")
        self.camera_pub = self.create_publisher(Image, "image", 10)
        timer_period = 1./30
        self.cap = cv2.VideoCapture(0)
        self.timer = self.create_timer(timer_period, self.timer_cb)
        self.bridge = CvBridge()
    def timer_cb(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        # todo: undistort
        try:
            image_msg = self.bridge.cv2_to_imgmsg(frame, encoding="passthrough")
        except CvBridgeError as e:
            print(e)
        image_msg.header.frame_id = "map"
        self.camera_pub.publish(image_msg)


def main(args=None):
    rclpy.init(args=args)

    camera_publisher = CameraPublisher()
    rclpy.spin(camera_publisher)

if __name__ == "__main__":
    main()
    