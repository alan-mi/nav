#!/usr/bin/env python
# coding: utf-8

import os

# from tools.detection import Detection
from std_msgs.msg import String

os.environ["ROS_MASTER_URI"] = "http://localhost:11311"
os.environ["ROS_PACKAGE_PATH"] = "/opt/ros/kinetic/share"

import rospy
rospy.init_node("pub")



pub = rospy.Publisher("/own/pub",String,queue_size=1)
if __name__ == '__main__':
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        pub.publish("hello i am pub")
        rate.sleep()
