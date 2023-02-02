import random
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin
import shapely
from shapely.geometry import LineString, Point

# not quite so Constant
num_rays = 10
num_bounces = 1
rect = [0,35,0,1] #x1,x2,y1,y2
eps = 0.01
xs_min = 15 + eps
xs_max = 35 - eps
ys_min = 0 + eps
ys_max = 1 - eps
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
n_out = 1
n_scinti = 1.58
crit_angle = np.arcsin(n_out/n_scinti)
escaped_count = 0
to_many_bounces_count = 0
detected_count = 0
no_outcome = 0
angle = 0
hit_border=0

def unit_vector(vector):
	return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
	v1_u = unit_vector(v1)
	v2_u = unit_vector(v2)
	print('angle')
	print(v1_u,v2_u)
	print('frrr')
	print(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))
	return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


#computes hit position
def intersects(start, angle):
	x1, y1 = start
	slope = np.tan(angle)
	#print(slope)
	x2 = x1 + (rect[1]+rect[3])*np.cos(angle)
	y2 = y1 + (rect[1]+rect[3])*np.sin(angle)
	line1 = LineString([(x1,y1),(x2,y2)])
	hit = False
	for i in range(4):
		print('\ntesting')
		print(i)
		int_pt = line1.intersection(border[i])
		try:
			hit = int_pt.x, int_pt.y # remember to exclude corner cases
			global hit_border
			hit_border=i
			return hit
		except:
			global no_outcome 
			no_outcome += 1
			print('no hit found\n')


# Monte Carlo loop
for i in range(num_rays):
	#start parameter
	x_pos = random.uniform(xs_min, xs_max)
	y_pos = random.uniform(ys_min, ys_max)
	angle = random.uniform(0, 2*np.pi)
	for j in range(num_bounces):
		hit = intersects((x_pos,y_pos), angle)
		print(hit_border)
		x2 = x_pos + (rect[1]+rect[3])*np.cos(angle)
		y2 = y_pos + (rect[1]+rect[3])*np.sin(angle)
		angle_check = angle_between((x2-x_pos,y2-y_pos),simple_border[hit_border])
		if angle_check  > crit_angle and angle_check  < np.pi-crit_angle:
			print('escaped')
			escaped_count += 1
			break
		if hit_border == 0:
			if angle < np.pi:
				angle = angle - 2*angle_check
			if angle > np.pi:
				angle = angle + 2*(np.pi*angle_check)
		if hit_border == 1:
			if angle < np.pi:
				angle = 2*np.pi - angle_check
			if angle > 0.5*np.pi:
				angle = angle + 2*(np.pi*angle_check)
		if hit_border == 2:
			if angle < np.pi:
				angle = angle + 2*(np.pi*angle_check)
			if angle > np.pi:
				angle = angle - 2*angle_check
		if hit_border == 3:
			if angle < 1.5*np.pi:
				angle = angle - 2*angle_check
			if angle > 1.5*np.pi:
				angle = np.pi - angle_check
		print('Starting params: x_pos={}, y_pos={}, angle={}'.format(x_pos, y_pos, angle))
		print('hit at')
		print(hit)
print(str(escaped_count) + ' escaped')
# Plot the light beam
#plt.plot(x, y, 'ro', markersize=0.5)
#plt.show()
