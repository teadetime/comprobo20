#!/usr/bin/env python3
from __future__ import print_function, division
import rospy
import copy
from neato_node.msg import Bump
from std_msgs.msg import Int8MultiArray
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Vector3
from visualization_msgs.msg import Marker
import math
import tty
import select
import sys
import termios
settings = termios.tcgetattr(sys.stdin)
key = None

class tele(object):
    def __init__(self):
        rospy.init_node('tele_nathan')
        rospy.Subscriber('/odom', Odometry, self.process_odom)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.linear_vel = 0.0
        self.angular_vel = 0.0
        self.state = "Start"
        self.turns = 4
        self.turn_target = 0 # Robot inits to zero
        self.distance_target = None
        self.pose = None
        self.turning = False
        self.driving = True
        self.start_time = None
        self.starting = True

    def process_odom(self, msg):
        self.pose = msg.pose.pose

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def run(self):
        r = rospy.Rate(100)
        self.start_time = rospy.Time.now()
        print(self.start_time, self.start_time + rospy.Duration(1))
        while not rospy.is_shutdown():
            if self.starting:
                self.linear_vel = 0
                self.angular_vel = 0
                self.starting = False
            elif self.turns > 0:
                if self.driving:
                    self.linear_vel = .2
                    print(rospy.Time.now(), (self.start_time + rospy.Duration(5)))
                    if rospy.Time.now() > (self.start_time + rospy.Duration(5)):
                        print("Drove a meter")
                        self.linear_vel = 0
                        self.driving = False
                        self.turning = True
                        self.start_time = rospy.Time.now()
                if self.turning:
                    self.angular_vel = math.pi/(2*3)
                    if rospy.Time.now() > self.start_time + rospy.Duration(3):
                        print("turned")
                        self.angular_vel = 0
                        self.driving = True
                        self.turning = False
                        self.turns -= 1
                        self.start_time = rospy.Time.now()


            # print(self.state)
            # if self.state == "Start":
            #     # Do Specific Start stuff
            #     if self.pose is not None:
            #         self.state = "Drive"
            #         self.distance_target = copy.deepcopy(self.pose)
            #         self.distance_target.position.y += 1
            #         self.linear_vel = .2
            # elif self.state == "Drive":
            #     #TODO:  Determine direction to determine which pose to check?
            #     print(self.pose.position.y, self.distance_target.position.y)
            #     if self.pose.position.y >= self.distance_target.position.y:
            #         self.linear_vel = 0
            #         self.angular_vel = 0
            #         self.state = "Turn"
            #         self.turn_target = self.pose.orientation.z + 90
            #         self.angular_vel = 0.1
            #     pass
            #     # Control loop to get the end dest
            # elif self.state == "Turn":
            #     #TODO: turn both ways?
            #
            #     # COntrol loop to switch
            #     pass
            # elif self.state == "Stop":
            #     pass
            #
            # key = self.getKey()
            # # USe arrow keys to increase velocity, space to stop
            # if key == " ":
            #     self.desired_vel = 0
            #     self.angular_vel = 0
            # elif key == 'A':
            #     self.linear_vel += .1
            # elif key == "B":
            #     self.linear_vel -= .1
            # if key == "C":
            #     self.angular_vel -= .1
            # elif key == "D":
            #     self.angular_vel += .1
            self.pub.publish(Twist(linear=Vector3(x=self.linear_vel),angular=Vector3(z=self.angular_vel)))
            r.sleep()
        self.pub.publish(Twist(angular=Vector3(z=self.angular_vel)))
        # self.pub.publish(Twist(linear=Vector3(x=0), angular=Vector3(z=0)))


if __name__ == '__main__':
    tele_nathan = tele()
    tele_nathan.run()

