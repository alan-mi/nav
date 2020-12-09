#!/usr/bin/env python
# coding: utf-8

import os

# from tools.detection import Detection

os.environ["ROS_MASTER_URI"] = "http://fanfan:11311"
os.environ["ROS_PACKAGE_PATH"] = "/opt/ros/kinetic/share"
import rospy
import move_base_msgs

import rospy
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Twist, Vector3
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from visualization_msgs.msg import Marker
from math import radians, pi

cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
cancel_pub = rospy.Publisher("/move_base/cancel", GoalID, queue_size=1)


def shutdown():
    su = Vector3(x=0, y=0, z=0)
    cmd = Twist(su, su)
    res = cmd_pub.publish(cmd)
    print res
    print("停止运行...")


def goal_id():
    stamp = genpy.Time()
    rospy.loginfo("取消任务")
    return GoalID(stamp, "")


if __name__ == '__main__':
    try:
        rospy.init_node("cancel")
        rospy.on_shutdown(shutdown)
        rate = rospy.Rate(5)
        for i in range(2):
            cancel_pub.publish(goal_id())
            rate.sleep()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
