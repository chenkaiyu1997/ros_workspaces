#!/usr/bin/env python
import sys
import rospy
import numpy as np
import traceback
import time

from moveit_msgs.msg import OrientationConstraint
from geometry_msgs.msg import PoseStamped

from path_planner import PathPlanner
from controller import Controller
from intera_interface import Limb

from planning.msg import ChouChou

queue = []
prev_msg = ""

def get_points(message):
	"""
	We will add the point we received to queue
	"""
	global prev_msg
	
	#print("9999",message.status_type)
	if prev_msg != message and message.status_type != "dummy":
		queue.append(message)
		prev_msg = message
		print('0000',queue,len(queue))

def main():
	plandraw = PathPlanner('right_arm')

	plandraw.start_position()

	while not rospy.is_shutdown():
		raw_input("~~~~~~~~~~~~!!!!!!!!!!!!")
		while not rospy.is_shutdown():
			try:
				while queue:
					cur = queue.pop(0)
					x,y,z = cur.position_x,cur.position_y,cur.position_z
					if cur.status_type != "edge_grad":
						# ti bi !!!!! luo bi !!!!
						if cur.status_type == "starting":
							print("start")
							goal_1 = PoseStamped()
							goal_1.header.frame_id = "base"

							#x, y, and z position
							goal_1.pose.position.x = x
							goal_1.pose.position.y = y
							goal_1.pose.position.z = z

							#Orientation as a quaternion
							goal_1.pose.orientation.x = 0.0
							goal_1.pose.orientation.y = 1.0
							goal_1.pose.orientation.z = 0.0
							goal_1.pose.orientation.w = 0.0

							plan = plandraw.plan_to_pose(goal_1, [])

							if not plandraw.execute_plan(plan):
								raise Exception("Execution failed")

						elif cur.status_type == "next_point":
							print("next")
							goal_1 = PoseStamped()
							goal_1.header.frame_id = "base"

							#x, y, and z position
							goal_1.pose.position.x = x
							goal_1.pose.position.y = y
							goal_1.pose.position.z = z

							#Orientation as a quaternion
							goal_1.pose.orientation.x = 0.0
							goal_1.pose.orientation.y = 1.0
							goal_1.pose.orientation.z = 0.0
							goal_1.pose.orientation.w = 0.0

							plan = plandraw.plan_to_pose(goal_1, [])

							if not plandraw.execute_plan(plan):
								raise Exception("Execution failed")
						elif cur.status_type == "ending":
							print("ti bi")
				raw_input("Press <Enter> to move next!!!")
			except Exception as e:
				print e
			else:
				print("lllllllllllllllllllll")
				break



if __name__ == '__main__':
	rospy.init_node('moveit_node')
	rospy.Subscriber("position_messages", ChouChou, get_points,queue_size=10)
	
	main()
	rospy.spin()
