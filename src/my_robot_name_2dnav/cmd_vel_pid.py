#!/usr/bin/env python
import rospy
import tf
import math
from geometry_msgs.msg import Twist, Point, Pose, PointStamped
from nav_msgs.msg import Odometry, Path
from move_base_msgs.msg import MoveBaseActionGoal

robot_pose = Pose()
robot_twist = Twist()
goal_pose = Pose()
goal_yaw = 0
local_path_position_list = []
local_path_yaw_list = []
controller_frequency = 5
max_vel_x = 1
max_vel_x_backwards = -0.3
min_vel_x = 0.1
max_vel_theta = 0.8
acc_lim_x = 0.5
acc_lim_theta = 0.1
xy_goal_tolerance = 0.5
yaw_goal_tolerance = 0.1
Kp = 0.15
Kd = 0

dead_band = False
last_vel_x = 0


def quaternion_2_euler(orientation):
    quaternion_list = [orientation.x, orientation.y, orientation.z, orientation.w]
    euler = tf.transformations.euler_from_quaternion(quaternion_list)
    return euler


def get_odometry(odom):
    global robot_pose, robot_twist
    robot_pose = odom.pose.pose
    robot_twist = odom.twist.twist
    # robot_orientation = robot_position.orientation
    # quaternion_list = [robot_orientation.x, robot_orientation.y, robot_orientation.z, robot_orientation.w]
    # robot_yaw = tf.transformations.euler_from_quaternion(quaternion_list)[2]


def get_local_plan(path):
    global local_path_position_list, local_path_yaw_list
    local_path_list = path.poses
    local_path_position_list = [Point()] * len(local_path_list)
    local_path_yaw_list = [0] * len(local_path_list)
    for i in range(len(local_path_list)):
        local_path_position_list[i] = local_path_list[i].pose.position
        local_path_yaw_list[i] = quaternion_2_euler(local_path_list[i].pose.orientation)[2]


def get_cmd_vel(cmd_vel):
    global dead_band
    vel_x = cmd_vel.linear.x
    vel_theta = cmd_vel.angular.z
    if vel_x == 0 and vel_theta == 1:
        dead_band = True
    else:
        dead_band = False


def get_move_base_goal(goal):
    global goal_pose, goal_yaw
    goal_pose = goal.goal.target_pose.pose
    goal_yaw = quaternion_2_euler(goal_pose.orientation)[2]


def compute_distance(position1, position2):
    distance = math.sqrt((position1.x - position2.x) ** 2 +
                         (position1.y - position2.y) ** 2)
    return distance


def compute_linear_vel(distance, dif_yaw):
    vel = 0.2 * distance
    if abs(dif_yaw) > math.pi/10:
        vel = 0
    elif vel > max_vel_x:
        vel = max_vel_x
    elif vel < max_vel_x_backwards:
        vel = max_vel_x
    elif abs(vel) < min_vel_x:
        vel = 0
    return vel


def compute_ang_vel(dif_yaw, dif_dif_yaw):
    vel = Kp * dif_yaw + Kd + dif_dif_yaw
    if abs(vel) > abs(max_vel_theta):
        vel = abs(vel) / vel * abs(max_vel_theta)
    return vel


pub_cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)
sub_odom = rospy.Subscriber('/odom', Odometry, get_odometry)
# sub_local_plan = rospy.Subscriber('/move_base/DWAPlannerROS/local_plan', Path, get_local_plan)
sub_local_plan = rospy.Subscriber('/move_base/TebLocalPlannerROS/local_plan', Path, get_local_plan)
sub_amd_vel = rospy.Subscriber('/cmd_vel_bak', Twist, get_cmd_vel)
sub_move_base_goal = rospy.Subscriber('/move_base/goal', MoveBaseActionGoal, get_move_base_goal)

rospy.init_node('cmd_vel_pid')
rate = rospy.Rate(controller_frequency)

while not rospy.is_shutdown():
    robot_position = robot_pose.position
    robot_yaw = quaternion_2_euler(robot_pose.orientation)[2]
    path_distance = 0
    current_dif_yaw = 0
    last_dif_yaw = 0
    if local_path_position_list and local_path_yaw_list:
        local_path_last_point_position = local_path_position_list[-1]
        local_path_last_point_yaw = local_path_yaw_list[len(local_path_yaw_list)//5]
        path_distance = compute_distance(robot_position, local_path_last_point_position)
        # path_distance = math.sqrt((robot_position.x - local_path_last_point_position.x) ** 2 +
        #                           (robot_position.y - local_path_last_point_position.y) ** 2)
        current_dif_yaw = local_path_last_point_yaw - robot_yaw
        if current_dif_yaw > math.pi:
            current_dif_yaw -= 2 * math.pi
        elif current_dif_yaw < -math.pi:
            current_dif_yaw += 2 * math.pi
        # print(local_path_position_list)
        # print(local_path_yaw_list)
        # print(path_distance)
        # print(current_dif_yaw)
        # print('\n')
    variation_dif_yaw = current_dif_yaw - last_dif_yaw

    dif_goal_distance = compute_distance(robot_position, goal_pose.position)
    dif_goal_yaw = goal_yaw - robot_yaw
    if dif_goal_distance < xy_goal_tolerance and abs(dif_goal_yaw) < yaw_goal_tolerance:
        linear_vel = 0
        ang_vel = 0
    elif dead_band:
        linear_vel = 0
        ang_vel = 0.5
    else:
        linear_vel = compute_linear_vel(path_distance, current_dif_yaw)
        ang_vel = compute_ang_vel(current_dif_yaw, variation_dif_yaw)

    vel_cmd = Twist()
    vel_cmd.linear.x = linear_vel
    vel_cmd.angular.z = ang_vel
    pub_cmd_vel.publish(vel_cmd)
    last_dif_yaw = current_dif_yaw
    rate.sleep()
