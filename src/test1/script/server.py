#!/usr/bin/env python
# coding: utf-8

import os
os.environ["ROS_MASTER_URI"] = "http://localhost:11311"
os.environ["ROS_PACKAGE_PATH"] = "/opt/ros/kinetic/share"

# from tools.detection import Detection
from test1.srv import AddTowInt,AddTowIntResponse, AddTowIntRequest

import rospy



def handle_add_tow_int(req):
    if isinstance(req,AddTowIntRequest):
        rospy.loginfo("a:{} b:{}".format(req.a,req.b))


    return AddTowIntResponse(req.a + req.b)


def add_tow_ints_server():
    rospy.init_node("add_tow_ints_serve")
    s = rospy.Service("add_tow_ints_serve", AddTowInt, handle_add_tow_int)
    rospy.loginfo("Ready to add two ints.")
    s.spin()


if __name__ == '__main__':

    add_tow_ints_server()
