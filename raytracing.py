import random
import matplotlib.pyplot as plt
import numpy as np
import shapely
from shapely.geometry import LineString, Point

# not quite so Constant
#number of rays and max bounces
num_rays = 100000
num_bounces = 100
#size of rectangle
rect = [0,35,0,1] #x1,x2,y1,y2
#size of incident area, eps is used to avoid starting on the edge(should be fine after first step should test)
eps = 0.0000000001
xs_min = 15 + eps
xs_max = 35 - eps
ys_min = 0 + eps
ys_max = 1 - eps
#different definitions of rectangle
a = (rect[0],rect[2])
b= (rect[0],rect[3])
c = (rect[1],rect[3])
d = (rect[1],rect[2])
left = LineString([a,b])
top = LineString([b,c])
right = LineString([c,d])
bottom = LineString([d,a])
border = [left, top, right, bottom]
left1 = (a,b)
top1 = (b,c)
right1 = (c,d)
bottom1 = (d,a)
simple_border = [(rect[0],rect[3]),(rect[1],rect[2]),(rect[0],0- rect[3]),(0-rect[1],rect[2])]
#refraction indices
n_out = 1
n_scinti = 1.58
crit_angle = np.arcsin(n_out/n_scinti)
#print('crit angle')
#print(np.rad2deg(crit_angle))
#counters to track final states
escaped_count = 0
to_many_bounces_count = 0
detected_count = 0
#global variables used for crossfunction info(i know it should be avoided)
no_outcome = 0
angle = 0
hit_border=0

def angle_between(v1, v2):
	cosang = np.dot(v1, v2)
	sinang = np.linalg.norm(np.cross(v1, v2))
	#print(cosang)
	return np.arctan2(sinang, cosang)

#computes hit position
def intersects(start, angle):
	global skip_border
	x1, y1 = start
	slope = np.tan(angle)
	#print(slope)
	x2 = x1 + (rect[1]+rect[3])*np.cos(angle)
	y2 = y1 + (rect[1]+rect[3])*np.sin(angle)
	line1 = LineString([(x1,y1),(x2,y2)])
	hit = False
	for i in range(4):
		#print('\ntesting')
		#print(i)
		int_pt = line1.intersection(border[i])
		if skip_border != i:
			try:
				hit = int_pt.x, int_pt.y # remember to exclude corner cases
				global hit_border
				hit_border=i
				skip_border = i
				x2 = x_pos + (rect[1]+rect[3])*np.cos(angle)
				y2 = y_pos + (rect[1]+rect[3])*np.sin(angle)
				#plot_step(x_pos,x2,y_pos,y2)
				return hit
			except:
				global no_outcome 
				#no_outcome += 1
				#print('no hit found\n')

#draws rectangle
def plot_box():
	x = np.linspace(rect[0],rect[0], 100)#x1,x2,y1,y2
	y = np.linspace(rect[2],rect[3], 100)
	ax.plot(x, y, linewidth=1.0, color="blue")
	x = np.linspace(rect[0],rect[1], 100)#x1,x2,y1,y2
	y = np.linspace(rect[3],rect[3], 100)
	ax.plot(x, y, linewidth=1.0, color="blue")
	x = np.linspace(rect[1],rect[1], 100)#x1,x2,y1,y2
	y = np.linspace(rect[2],rect[3], 100)
	ax.plot(x, y, linewidth=1.0, color="blue")
	x = np.linspace(rect[0],rect[1], 100)#x1,x2,y1,y2
	y = np.linspace(rect[2],rect[2], 100)
	ax.plot(x, y, linewidth=1.0, color="blue")
	ax.set(xlim=(rect[0] - 0.1*rect[1], rect[1] + 0.1*rect[1]), ylim=(rect[2] - 0.1*rect[3], rect[3] + 0.1*rect[3]))
	#ax.set(xlim=(-50, 50), ylim=(-50, 50))

#draws light ray
def plot_step(x1,x2,y1,y2):#,color
	x = np.linspace(x1,x2, 100)#x1,x2,y1,y2
	y = np.linspace(y1,y2, 100)
	ax.plot(x, y, linewidth=1.0, label='1')#, color=color)

def detection():
	i=1

# Monte Carlo loop
for i in range(num_rays):
	print(i)
	#start parameter
	skip_border = 5
	x_pos = random.uniform(xs_min, xs_max)
	y_pos = random.uniform(ys_min, ys_max)
	angle = random.uniform(0, 2*np.pi)
	#fig, ax = plt.subplots()
	#plot_box()
	#print('Starting params: x_pos={}, y_pos={}, angle={}'.format(x_pos, y_pos, angle))
	for j in range(num_bounces):
		#print('this is', j)
		hit = intersects((x_pos,y_pos), angle)
		skip_border=hit_border
		#print(hit_border)
		x2 = x_pos + (rect[1]+rect[3])*np.cos(angle)
		y2 = y_pos + (rect[1]+rect[3])*np.sin(angle)
		angle_check = angle_between((x2-x_pos,y2-y_pos),simple_border[hit_border])
		#print('check angle')
		#print(x_pos,y_pos)
		#print(x2,y2)
		#print('difference')
		#print((x2-x_pos,y2-y_pos),simple_border[hit_border])
		#print(np.rad2deg(angle_check))
		'''
		'''
		if angle_check  > crit_angle and angle_check  < np.pi-crit_angle:
			print('escaped')
			escaped_count += 1
			break
		
		if hit_border == 0:
			if angle < np.pi:
				angle = angle - 2*angle_check
			if angle > np.pi:
				angle = angle + 2*(np.pi-angle_check)
		if hit_border == 1:
			if angle < 0.5*np.pi:
				angle = 2*np.pi - angle_check
			if angle > 0.5*np.pi:
				angle = 2*np.pi - angle_check
				#angle = angle + 2*(np.pi*angle_check)
		if hit_border == 2:
			if angle < np.pi:
				angle = angle + 2*(np.pi-angle_check)
			if angle > np.pi:
				angle = angle - 2*angle_check
		if hit_border == 3:
			if angle < 1.5*np.pi:
				angle = angle - 2*angle_check
			if angle > 1.5*np.pi:
				angle = np.pi - angle_check
		#print('hit')
		#print(hit)
		try:
			x_pos = hit[0]
			y_pos = hit[1]
		except:
			no_outcome += 1
			break
		x2 = x_pos + (rect[1]+rect[3])*np.cos(angle)
		y2 = y_pos + (rect[1]+rect[3])*np.sin(angle)
		#plot_step(x_pos,x2,y_pos,y2)
		#print('updated params: x_pos={}, y_pos={}, angle={}'.format(x_pos, y_pos, angle))
		if j+1 == num_bounces:
			to_many_bounces_count += 1
	#ax.legend()
	#plt.show()

		
print(str(escaped_count) + ' escaped')
print(str(no_outcome) + ' no outcomes')
print(str(to_many_bounces_count) + ' to many bounces')
