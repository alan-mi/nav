#!/usr/bin/env python
# coding: utf-8

import os

# from tools.detection import Detection
from std_msgs.msg import String

os.environ["ROS_MASTER_URI"] = "http://localhost:11311"
os.environ["ROS_PACKAGE_PATH"] = "/opt/ros/kinetic/share"

import rospy
rospy.init_node("sub")

def sub_callback(msg):
    print(msg.data)

if __name__ == '__main__':
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        sub = rospy.Subscriber("/pub",String,callback=sub_callback)