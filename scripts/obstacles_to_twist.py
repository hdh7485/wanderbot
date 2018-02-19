#!/usr/bin/env python
import rospy
from obstacle_detector.msg import Obstacles
from geometry_msgs.msg import PointStamped

pub_left = rospy.Publisher('left_point', PointStamped, queue_size=10)
pub_right = rospy.Publisher('right_point', PointStamped, queue_size=10)
pub_center = rospy.Publisher('center_point', PointStamped, queue_size=10)

def obstacle_callback(data):
	global pub
#	rospy.loginfo(data)
	left_far = PointStamped()
	left_far.header.stamp = rospy.Time.now()
	left_far.header.frame_id = "base_link"

	right_far = PointStamped()
	right_far.header.stamp = rospy.Time.now()
	right_far.header.frame_id = "base_link"

	center_point = PointStamped()
	center_point.header.stamp = rospy.Time.now()
	center_point.header.frame_id = "base_link"

	for circle in data.circles:
		if circle.center.y < left_far.point.y:
			left_far.point.x = circle.center.x
			left_far.point.y = circle.center.y
		if circle.center.y > right_far.point.y:
			right_far.point.x = circle.center.x
			right_far.point.y = circle.center.y
	center_point.point.x = (right_far.point.x + left_far.point.x)/2
	center_point.point.y = (right_far.point.y + left_far.point.y)/2
	pub_left.publish(left_far)
	pub_right.publish(right_far)
	pub_center.publish(center_point)
	rospy.loginfo(center_point)

def listener():
	rospy.init_node('obstacle_to_twist', anonymous=True)
	sub = rospy.Subscriber('obstacles', Obstacles, obstacle_callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
