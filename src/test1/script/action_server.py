#!/usr/bin/env python
# coding: utf-8

import os
os.environ["ROS_MASTER_URI"] = "http://water:11311"
os.environ["ROS_PACKAGE_PATH"] = "/opt/ros/kinetic/share"


import rospy

import actionlib

from test1.msg import DoDishesAction,DoDishesGoal,DoDishesFeedback,DoDishesResult

class DoDishesServer():
    def __init__(self):
        self.server = actionlib.SimpleActionServer("do_dishes", DoDishesAction, self.execute, False)
        self.feedback = DoDishesFeedback()
        self.feedback.percent_complete = 0
        self.rate = rospy.Rate(1)
        self.server.start()

    def execute(self, goal):
        success = True
        if goal.dishwasher_id is 0:
            self.server.set_aborted()
            success = False

        else:
            for i in range(goal.dishwasher_id):
                if self.server.is_preempt_requested():
                    self.server.set_preempted()
                    success = False
                    rospy.loginfo("被抢占了")
                    break
                self.feedback.percent_complete = (float(i)/float(goal.dishwasher_id))
                self.server.publish_feedback(self.feedback)
                self.rate.sleep()
            if success:
                res = DoDishesResult()
                res.total_dishes_cleaned = goal.dishwasher_id
                self.server.set_succeeded(res)

if __name__ == '__main__':
    rospy.init_node('do_dishes_server')
    server = DoDishesServer()
    rospy.spin()