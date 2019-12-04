#!/usr/bin/env python
import sys
import rospy
from geometry_msgs.msg import Twist
PI=3.14

def turtle_controller():
	rospy.init_node('turtle_controller', anonymous=True)
	pub = rospy.Publisher('/'+sys.argv[-1]+'/cmd_vel', Twist, queue_size=10)
	vel_msg = Twist()

	vel_msg.linear.x = 0
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0

	while not rospy.is_shutdown():
		inst = raw_input()
		if inst == 'w':
			vel_msg.linear.x = 1
			vel_msg.angular.z = 0
		elif inst == 'a':
			vel_msg.angular.z = 90*2*PI/360
			vel_msg.linear.x = 0
		elif inst == 's':
			vel_msg.linear.x = -1
			vel_msg.angular.z = 0
		elif inst == 'd':
			vel_msg.angular.z = -90*2*PI/360
			vel_msg.linear.x = 0

		pub.publish(vel_msg)





if __name__ == '__main__':
	try:
		turtle_controller()
	except rospy.ROSInterruptException:
		raise