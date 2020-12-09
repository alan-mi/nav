#!/usr/bin/env python
# coding: utf-8

import os

os.environ["ROS_MASTER_URI"] = "http://localhost:11311"
os.environ["ROS_PACKAGE_PATH"] = "/opt/ros/kinetic/share"

import rospy
import actionlib
from actionlib import GoalStatus
import test1.msg


def done_cb(state, result):
    rospy.loginfo(state)
    rospy.loginfo(result)

    if state == GoalStatus.ABORTED:
        rospy.loginfo("server working error, don't finish my job.")
    elif state == GoalStatus.PREEMPTED:
        rospy.loginfo("client cancel job.")
    elif state == GoalStatus.SUCCEEDED:
        rospy.loginfo("server finish job.")
        rospy.loginfo("result: {}" .format(result))


def active_cb():
    rospy.loginfo("active callback")


def feedback_cb(feedback):
    # rospy.loginfo(feedback)
    if len(feedback.sequence) == 10:
        global client
        client.cancel_goal()
        pass
    print feedback.sequence


def fibonacci_client():

    client = actionlib.SimpleActionClient("fibonacci", test1.msg.FibonacciAction)
    client.wait_for_server()
    goal = test1.msg.FibonacciGoal(order=20)
    client.send_goal(goal, feedback_cb=feedback_cb, active_cb=active_cb, done_cb=done_cb)

    client.wait_for_result()
    return client.get_result()


if __name__ == '__main__':
    rospy.init_node("fib_py")
    client = actionlib.SimpleActionClient("fibonacci", test1.msg.FibonacciAction)
    client.wait_for_server()
    goal = test1.msg.FibonacciGoal(order=0)
    client.send_goal(goal, feedback_cb=feedback_cb, active_cb=active_cb, done_cb=done_cb)

    client.wait_for_result()
    print client.get_result()
    client.cancel_goal()
