import sys, os
import random

import simplejson as json

import numpy
from numpy import *

from utils.printing import heading
from utils.helper_functions import clamp

class PlasmaNoise():
	def __init__(self, max_iterations):
		self.random_seed = 101
		self.max_iterations = max_iterations
		self.current_iteration = self.max_iterations
		self.vertical_mult = 1.0
		self.vertical_error = 0.2
		self.image_size = int(power(2, self.max_iterations))

		#random.seed(self.random_seed)
		self.rand = random.random

		self.noise_map = zeros((self.image_size, self.image_size))

	def generate(self):
		print heading("Generating plasma noise")
		print self.image_size, self.noise_map.shape

		a = (0, 0)
		b = (self.image_size - 1, 0)
		c = (0, self.image_size - 1)
		d = (self.image_size - 1, self.image_size -1)

		self.subdivide(a, b, c, d)
		im = array(self.noise_map * 255, dtype = uint8)
		print im
		return im
		

	# Points are defined as (x, y) tuples.
	# {a, b, c, d} are corners such that:
	# a----b
	# |    |
	# c----d
	def subdivide(self, a, b, c, d):
		#print heading('START SUBDIVIDE', '-')
		#print 'a',a,'b', b, 'b', c, 'd', d

		length = int(b[0] - a[0]) 
		offset = int(length/2)

		# Recursive termination condition
		if length <= 1:
			return

		# Midpoint step
		mid_x = int(offset + a[0])
		mid_y = int(offset + a[1])
		mid = (mid_x, mid_y)

		#Calculate the value of the midpoint pixel
		point_average = average(
			(
				self.noise_map[a],
				self.noise_map[b],
				self.noise_map[c],
				self.noise_map[d]
			)
		)
		point_scaling = (float(length)/float(self.image_size)) * (random.random() - 0.5)
		point_value = point_average + 2.0 * point_scaling
		point_value = clamp(point_value, 0.0, 1.0)
		self.noise_map[mid] = point_value 

		# Diamond Step
		# Calculate the average of the corners and store the values
		self.noise_map[mid_x - offset, mid_y] = average(
			(
				self.noise_map[a],
				self.noise_map[c]
			)
		)
		self.noise_map[mid_x, mid_y - offset] = average(
			(
				self.noise_map[a],
				self.noise_map[b]
			)
		)
		self.noise_map[mid_x + offset, mid_y] = average(
			(
				self.noise_map[b],
				self.noise_map[d]
			)
		)
		self.noise_map[mid_x, mid_y + offset] = average(
			(
				self.noise_map[c],
				self.noise_map[d]
			)
		)

		#Recursive call
		self.subdivide(
			mid,
			(d[0], mid_y),
			(mid_x, d[1]),
			d
		)
		self.subdivide(
			(c[0], mid_y),
			mid,
			c,
			(mid_x, c[1])
		)
		self.subdivide(
			(mid_x, b[1]),
			b,
			mid,
			(b[0], mid_y)
		)
		self.subdivide(
			a,
			(mid_x, a[1]),
			(a[0], mid_y),
			mid
		)
	
if __name__ == "__main__":
	print "START"
	generator = PlasmaNoise()
	noise = generator.generate()
	set_printoptions(precision=3)

	print(noise)
	print "END"
