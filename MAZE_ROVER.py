import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class MazeRover:
    def __init__(self):
        rospy.init_node('maze_rover')
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.twist = Twist()
        self.rate = rospy.Rate(10)

    def scan_callback(self, data):

        desired_range = 0.5

        stop_threshold = 0.2

        range_index = len(data.ranges) / 2
        average_range = sum(data.ranges[range_index-10:range_index+10]) / 20


        if average_range > desired_range:
            self.twist.linear.x = 0.2
            self.twist.angular.z = 0.0

        else:
            left_range = sum(data.ranges[range_index+10:range_index+20]) / 10
            right_range = sum(data.ranges[range_index-20:range_index-10]) / 10
            if left_range > right_range:
                self.twist.angular.z = 0.2
            else:
                self.twist.angular.z = -0.2
            self.twist.linear.x = 0.0


        if min(data.ranges) < stop_threshold:
            self.twist.linear.x = 0.0

        self.cmd_vel_pub.publish(self.twist)

if __name__ == '__main__':
    rover = MazeRover()
    rospy.spin()

