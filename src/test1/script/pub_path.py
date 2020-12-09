#!/usr/bin/env python
# coding: utf-8

import os
os.environ["ROS_MASTER_URI"] = "http://localhost:11311"
os.environ["ROS_PACKAGE_PATH"] = "/opt/ros/kinetic/share"

# from tools.detection import Detection

import rospy
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import Pose, Twist, Vector3, PoseStamped, genpy
import math

if __name__ == '__main__':
    rospy.init_node("pus")
    ti = genpy.Time()
    print(ti.nsecs)
    path_pub = rospy.Publisher("trajectory", Path, queue_size=1)
    f = 0.0
    rate = rospy.Rate(1)
    lo_path = Path()
    lo_path.header.frame_id = "/my_frame"
    this_pose_stamped = PoseStamped()
    a = 0
    while not rospy.is_shutdown():
        lo_path.header.stamp = rospy.Time.now()
        # lo_path.header.seq = 0
        for i in range(1):
            # y = 5 * math.sin(f + i /100.0 * 2 * math.pi)
            # x = 5 * math.sin(f + i/100.0 * 2 * math.pi)
            # x = f + i
            a += 1
            x = a/20.0 + f
            y =  math.sin(x)
            this_pose_stamped  =  PoseStamped()
            this_pose_stamped.pose.position.x = x
            this_pose_stamped.pose.position.y = y
            this_pose_stamped.pose.orientation.x = 0
            this_pose_stamped.pose.orientation.y = 0
            this_pose_stamped.pose.orientation.z = 0
            this_pose_stamped.pose.orientation.w = 1
            this_pose_stamped.header.stamp = rospy.Time.now()
            this_pose_stamped.header.frame_id = "/my_frame"
            if x > 6:
                break
            lo_path.poses.append(this_pose_stamped)
            print(len(lo_path.poses))
        # lo_path.header.stamp = rospy.Time.now()
        # for i in lo_path.poses:
        #     i.header.stamp = rospy.Time.now()
        if len(lo_path.poses) == 0:
            print "完成..."
            break
        path_pub.publish(lo_path)
        rate.sleep()
        f += 0.1
    # print(Path())
