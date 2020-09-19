#!/usr/bin/env python3

from __future__ import print_function, division
import rospy
from neato_node.msg import Bump
from std_msgs.msg import Int8MultiArray
from geometry_msgs.msg import Twist, Vector3
from visualization_msgs.msg import Marker

class EmergencyStopNode(object):
    def __init__(self):
        rospy.init_node('marker')
        rospy.Subscriber('/bump', Int8MultiArray, self.process_bump)
        #self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.blockpub = rospy.Publisher('/visualization_marker', Marker, queue_size=10)
        self.desired_velocity = 0.3
        self.marker = Marker()
        self.marker.header.frame_id = "base_link"
        self.marker.header.stamp = rospy.Time.now()
        self.marker.ns = "my_namespace"
        self.marker.id = 0
        self.marker.type = Marker.SPHERE
        self.marker.action = Marker.ADD
        self.marker.pose.position.x = 1
        self.marker.pose.position.y = 1
        self.marker.pose.position.z = 1
        self.marker.pose.orientation.x = 0.0
        self.marker.pose.orientation.y = 0.0
        self.marker.pose.orientation.z = 0.0
        self.marker.pose.orientation.w = 1.0
        self.marker.scale.x = 1
        self.marker.scale.y = 0.1
        self.marker.scale.z = 0.1
        self.marker.color.a = 1.0 # Don't forget to set the alpha!
        self.marker.color.r = 0.0
        self.marker.color.g = 1.0
        self.marker.color.b = 0.0
    def process_bump(self, msg):
        print(msg)
        if any((msg.data[0], msg.data[1], msg.data[2], msg.data[3])):
            self.desired_velocity = 0.0
            print("stop")

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            #self.pub.publish(Twist(linear=Vector3(x=self.desired_velocity)))
            self.blockpub.publish(self.marker)
            r.sleep()

if __name__ == '__main__':
    estop = EmergencyStopNode()
    estop.run()
