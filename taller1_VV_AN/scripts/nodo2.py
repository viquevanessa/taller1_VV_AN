#!/usr/bin/python
import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan
class Nodo2():


	def __init__(self):
		self.rospy = rospy
		self.rospy.init_node('nodo_2', anonymous = True)
		self.initParameters()
		self.initSubscribers()
		self.initPublishers()
		self.main()


	def initParameters(self):
		self.topic_scan = "/scan"
		self.topic_aux = "/aux_topic"
		self.A=[]
		self.datos=[]
		self.angulo=[]
		self.X=[]
		self.Y=[]
		self.dist=[]
		self.msg_aux = Bool()
		self.msg_scan = LaserScan()
		self.cambio_scan = False
		self.rate = self.rospy.Rate(50)

	def callback_scan(self, msg):
		self.msg_scan = msg.header
		self.msg_scan = msg.angle_min
		self.msg_scan = msg.angle_max
		self.msg_scan = msg.ranges
		self.msg_scan = msg.range_min
		self.msg_scan = msg.range_max
		self.msg_scan = msg.angle_increment
		self.cambio_scan = True
		self.A=[msg.ranges, msg.angle_increment, msg.angle_max, msg.range_min, msg.angle_min, msg.range_max]
		return

	def initSubscribers(self):
		self.sub_scan = self.rospy.Subscriber(self.topic_scan, LaserScan, self.callback_scan)
		return

	def initPublishers(self):
		self.pub_aux = self.rospy.Publisher(self.topic_aux, Bool, queue_size=10)
		return

	def main(self):
		while not self.rospy.is_shutdown():
			if self.cambio_scan:
				self.dist = []
				self.X = []
				self.Y = []
				self.datosX = []
				self.datosY = []
				self.acum = []
				for i in range(0,len(self.A[0])):
					self.angulo.append(self.A[4] + (i*self.A[1]))
					self.X.append((self.A[0][i])*math.cos(self.angulo[i]))
					self.Y.append((self.A[0][i])*math.sin(self.angulo[i]))

				for a in range(0, len(self.Y)):
					if self.Y[a] <= 0.05 and self.Y[a] >= 0.0:
						self.datosY.append(self.Y[a])
						self.datosX.append(self.Y[a])
				cont = 1
				k = 0
				flag2 = False
				for j in range(1,len(self.datosX)):
					self.dist.append(math.sqrt((self.datosX[j]-self.datosX[j-1])**2+(self.datosY[j]-self.datosY[j-1])**2))
					if self.dist[k] <= 0.1:
						cont = cont+1
					else:
						self.acum.append(cont)
						cont = 0
						flag2 = True
					k+=1
				if not flag2:
					self.acum.append(cont)
				flag = False
				for l in self.acum:
					if l >= 5:
						flag = True
				self.msg_aux.data = flag
				self.pub_aux.publish(self.msg_aux)
				self.cambio_scan = False
				self.rate.sleep()
		return

if __name__ == "__main__":
	try:
		print("Iniciando Nodo")
		nodo = Nodo2()
	except rospy.ROSInterruptException:
		print("Finalizando Nodo")
		pass
