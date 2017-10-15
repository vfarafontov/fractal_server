from PIL import Image

from utils import logger
from noise import plasma_noise

class NoiseConstructor():
	def __init__(self, logger):
		self.logger = logger

	def generate_plasma(self):
		ITERATIONS = 6
		generator = plasma_noise.PlasmaNoise(ITERATIONS)
		noise_map = generator.generate()

		img = Image.fromarray(noisemap)

if __name__ == "__main__":
	print "START"

	logger = logger.Logger("CRIT", "./logs", "noise_test.log")
	noise = Noise(logger)

	print "END"
