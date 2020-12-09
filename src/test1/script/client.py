#!/usr/bin/env python
# coding: utf-8

import os

from test1.srv import AddTowInt, AddTowIntRequest

# from tools.detection import Detection

os.environ["ROS_MASTER_URI"] = "http://localhost:11311"
os.environ["ROS_PACKAGE_PATH"] = "/opt/ros/melodic/share"

import rospy


def add_tow_ints_client(x, y):
    rospy.wait_for_service("add_tow_ints_serve")
    try:
        add_tow_ints = rospy.ServiceProxy("add_tow_ints_serve", AddTowInt)

        # print add_tow_ints.call(x,y)
        a = AddTowIntRequest()
        a.a = x
        a.b = y
        print add_tow_ints(a)
        resp1 = add_tow_ints(x, y)
        return resp1.sum
    except rospy.ServiceException as e:
        print e


if __name__ == '__main__':
    print(add_tow_ints_client(90, 10))
