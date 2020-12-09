#!/usr/bin/env python
# coding: utf-8

import os
from math import pi

os.environ["ROS_MASTER_URI"] = "http://localhost:11311"
os.environ["ROS_PACKAGE_PATH"] = "/opt/ros/kinetic/share"

# from tools.detection import Detection

import rospy
from nav_msgs.srv import GetPlan,GetPlanRequest,GetPlanResponse
from geometry_msgs.msg import PoseStamped,PointStamped
from move_base_msgs.msg import MoveBaseActionGoal
from tf.transformations import quaternion_from_euler,euler_from_quaternion
# euler xyz
# quaternion xyzw
from rospy import ServiceProxy

import tf
from nav_msgs.msg import Path

class Robot:
    def __init__(self):
        self.tf_listener = tf.TransformListener()
        try:
            self.tf_listener.waitForTransform('/map', '/base_link', rospy.Time(), rospy.Duration(6))
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            return

    def get_pos(self):
        try:
            (trans, rot) = self.tf_listener.lookupTransform('/map', '/base_link', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.loginfo("tf Error")
            return None
        # print rot


        euler = tf.transformations.euler_from_quaternion(rot)
        #print euler[2] / pi * 180

        x = trans[0]
        y = trans[1]
        th = euler[2] / pi * 180
        return (x, y, rot)



def clicked_point(msg):
    # rospy.loginfo(msg)
    goal_pub = rospy.Publisher("/goal",MoveBaseActionGoal,queue_size=1)
    plan_client = ServiceProxy("/move_base/make_plan",GetPlan)


    goalPos = PoseStamped()
    goalPos.header.frame_id = "map"
    goalPos.header.stamp = rospy.Time.now()
    goalPos.pose.position.x = msg.point.x
    goalPos.pose.position.y = msg.point.y
    goalPos.pose.orientation.x = rot[0]
    goalPos.pose.orientation.y = rot[1]
    goalPos.pose.orientation.z = rot[2]
    goalPos.pose.orientation.w = rot[3]

    getplan = GetPlanRequest()
    getplan.start.header.frame_id = "map"
    getplan.start.header.stamp = rospy.Time.now()
    getplan.start.pose.position.x = x
    getplan.start.pose.position.y = y
    getplan.start.pose.orientation.x = 0
    getplan.start.pose.orientation.y = 0
    getplan.start.pose.orientation.z = 0
    getplan.start.pose.orientation.w = 1
    getplan.goal = goalPos
    getplan.tolerance = 0.5

    goal = MoveBaseActionGoal()
    goal.goal.target_pose = goalPos
    goal.header.frame_id = "map"
    goal.header.stamp =  rospy.Time.now()
    goal_pub.publish(goal)

    res = plan_client.call(getplan)
    rospy.loginfo(res.plan.header.frame_id)
    path_pub = rospy.Publisher("trajectory", Path, queue_size=1)
    if isinstance(res, GetPlanResponse):
        res.plan.header.frame_id = "map"
        # res.plan.header.stamp = rospy.Time.now()
    path_pub.publish(res.plan)
    while True:

        plan_pub = rospy.Publisher("/move_base/GlobalPlanner/plan", Path, queue_size=1)
        plan_pub.publish(res.plan)



    # if isinstance(msg,PoseStamped):


if __name__ == '__main__':
    rospy.init_node("get_plan_node")
    rospy.loginfo("等待server")

    rospy.wait_for_service("/move_base/make_plan")
    rospy.Subscriber("/clicked_point",PointStamped,clicked_point)
    r = rospy.Rate(100)
    r.sleep()
    robot = Robot()
    while not rospy.is_shutdown():
        r.sleep()
        (x,y,rot) =  robot.get_pos()
