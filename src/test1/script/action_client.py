#!/usr/bin/env python
# coding: utf-8

import os

os.environ["ROS_MASTER_URI"] = "http://water:11311"
os.environ["ROS_PACKAGE_PATH"] = "/opt/ros/kinetic/share"

import rospy
import actionlib

from test1.msg import DoDishesAction, DoDishesGoal

def feedback(feedback):
    rospy.loginfo("已经完成{:.2%}".format(feedback.percent_complete))

def done(state,res):
    if state == actionlib.GoalStatus.ABORTED:
        rospy.loginfo("server working error, don't finish my job.")
        client.cancel_goal()

    elif state == actionlib.GoalStatus.PREEMPTED:
        rospy.loginfo("client cancel job.")
        client.cancel_goal()
    elif state == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("server finish job.")
        rospy.loginfo("result: {}".format(res))
    # print res
client = actionlib.SimpleActionClient("do_dishes", DoDishesAction)

if __name__ == '__main__':
    rospy.init_node("do_dishes_client")

    client.wait_for_server()

    goal = DoDishesGoal()
    goal.dishwasher_id = 10
    client.send_goal(goal,feedback_cb=feedback,done_cb=done)
    res = client.wait_for_result()
    print client.get_result()
    print res
    r = rospy.Rate(10)
    r.sleep()
