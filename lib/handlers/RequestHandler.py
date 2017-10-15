# FIRST PARTY IMPORTS
import os, sys
import traceback

# SECOND PARTY IMPORTS
import tornado.ioloop
import tornado.web

from PIL import Image
import simplejson as json

# THIRD PARTY IMPORTS
sys.path.append("./lib")
from noise import plasma_noise

from noise import voronoi
from noise import mandle

class MainHandler(tornado.web.RequestHandler):
	def initialize(self, logger):
		self.logger = logger

	#####################
	# UTILITY FUNCTIONS #
	#####################
	def parse_arguments(self):
		noise_type = str(self.get_argument('type'))
		iterations = int(self.get_argument('iter'))
		size = int(self.get_argument('size'))
		return noise_type, iterations, size	

	def get(self):
		self.logger.log("CRIT", "###################")
		self.logger.log("CRIT", "# FRACTAL REQUEST #")
		self.logger.log("CRIT", "###################")

		try:
			noise_type, iterations, size = self.parse_arguments()
		except Exception as e:
			error = {
				"ERROR": "Unable to get arguments",
				"EXCEPTION:": str(e)
			}
			self.logger.log("CRIT", json.dumps(error))
			self.write(json.dumps(error))
			self.finish()
			return

		self.logger.log("CRIT",  "{} {} {}".format(
			noise_type,
			iterations, size
		))

		try:
			if noise_type == 'mandle':
				img = mandle.mandlebrot(iterations, size)
				raw_img = img.save('test.png')
				self.logger.log("CRIT", raw_img)
				self.logger.log("CRIT", 'OK - Img done')

				file = open('test.png')
				data = file.read()
				file.close()

				self.set_header('Content-type', 'image/png')
				self.set_header('Content-length', len(data))
				self.write(data)
				self.finish()

			elif noise_type == 'plasma':
				os.system('rm test_plasma.png')

				plasma_generator = plasma_noise.PlasmaNoise(iterations)
				noise_map = plasma_generator.generate()

				img = Image.fromarray(noise_map)
				img.save('test_plasma.png', 'png')
				
				file = open('test_plasma.png')
				data = file.read()
				file.close()
				
			elif noise_type == 'voronoi':
				voronoi_generator = voronoi.Voronoi(size)
				noise_map = voronoi_generator.generate()

				img = Image.fromarray(noise_map)
				img.save('voronoi.png', 'png')

				file = open('voronoi.png', 'r')
				data = file.read()
				file.close()

		except Exception as e:
			exception = str(e)
			trace = str(traceback.format_exc())
			error = {
				"ERROR": "Error generating noise",
				"EXCEPTION": exception,
				"TRACE": trace
			}
			self.write(json.dumps(error))
			self.finish
			return

		self.set_header('Content-type', 'image/png')
		self.set_header('Content-length', len(data))
		self.write(data)
		self.finish()


