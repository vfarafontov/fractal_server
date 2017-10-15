import sys, os
import random

import simplejson as json

import numpy
from numpy import *

from utils.printing import heading

class Voronoi():
	def __init__(self, size):
		self.params = {
			"random_seed": 101,
			"image_size": int(power(2, size)),
			"num_points": 100
		}
		#random.seed(self.params['random_seed']
		self.rand = random.random
		self.noise_map = zeros((
			self.params['image_size'],
			self.params['image_size']
		))

	def gen_rand_point(self, index):
		return {
			"cords": array((
				int(self.params['image_size'] * self.rand()),
				int(self.params['image_size'] * self.rand())
			)),
			"color": float(index)/float(self.params['num_points'])
		}

	def generate(self):
		rand_points = []
		for index in range(0, self.params['num_points']):
			rand_points.append(self.gen_rand_point(index))

		size = self.params['image_size'] - 1

		for x in range(0, size):
			for y in range(0, size):
				pixel_membership = {
					"point": None,
					"distance": self.params['image_size']
				}

				for rand_point in rand_points:
					distance = linalg.norm(array((x,y)) - rand_point['cords'])
					if distance < pixel_membership['distance']:
						pixel_membership['point'] = rand_point
						pixel_membership['distance'] = distance

				self.noise_map[x][y] = pixel_membership['point']['color']
		im = array(self.noise_map * 255, dtype=uint8)
		print im
		return im	

def run():
	print "START"
	generator = Voronoi(4)
	print generator.generate()
	print "END"

if __name__ == "__main__":
	run()
