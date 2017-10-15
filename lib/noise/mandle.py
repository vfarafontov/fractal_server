from PIL import Image
import math, random
import threading
#import images2gif

class Point:
	def __init__(self, xCord, yCord):
		self.x = xCord;
		self.y = yCord;
	def setx(self, xCord):
		self.x = xCord;
	def sety(self, yCord):
		self.y = yCord;
	def get(self):
		return (self.x, self.y);
	def getx(self):
		return self.x;
	def gety(self):
		return self.y;
	def move(self, dx, dy):
		self.x += dx;
		self.y += dy;
	def echo(self):
		print('('+str(self.x)+','+str(self.y)+')');
		
def convertPoint(aPoint, width, height):
	x, y = aPoint.get();
	x = (x/float(width)*5.0)-2.5;
	y = (y/float(height)*5.0)-2.5;

	aPoint.setx(x);
	aPoint.sety(y);
	
	return aPoint;

def calc_at_pixel(x, y, width, height, max_iteration, aPoint, image, stepStrength, testIter):
	pointZero = convertPoint(Point(x,y), width, height);
	point = Point(0,0);

	iteration = 0;
	max_iteration = int(getDistance(aPoint, Point(x, y))/getDistance(Point(0,0), Point(width, height)) * max_iteration) + 1;
	while (point.getx()*point.getx() + point.gety()*point.gety() < 2*2) and (iteration < max_iteration):				
		xTemp = point.getx()*point.getx() - point.gety()*point.gety() + pointZero.getx();
		point.sety(2.0*point.getx()*point.gety()+pointZero.gety());
		point.setx(xTemp);

		iteration = iteration + 1;

	colVal = int(float(iteration)/float(max_iteration)*255.0 + image.getpixel((x,y))[0]);
	image.putpixel((x,y), (colVal, colVal, colVal));

def genMandlebrot(width, height, max_iteration, aPoint):
	image = Image.new("RGB", (width, height), "black")
	stepStrength = float(1.0)/float(max_iteration);
	testIter = max_iteration;
	threads = []
	for y in range(height):
		for x in range(width):
			worker = threading.Thread(
				target=calc_at_pixel,
				args=(x, y, width, height, max_iteration, aPoint, image, stepStrength, testIter,)
			)
			worker.setDaemon(True)
			threads.append(worker)
			worker.start()
	for thread in threads:
		thread.join()
	return image;

def getDistance(p1, p2):
	return math.sqrt(math.pow(p2.getx()-p1.getx(),2)+math.pow(p2.gety()-p1.gety(), 2));
		
def distanceImg(width, height, center):
	image = Image.new("RGB", (width, height), "black");
	dmax = math.sqrt(width*width + height*height);
	for y in range(height):
		for x in range(width):
			distance = math.sqrt(math.pow(center.getx()-x,2)+math.pow(center.gety()-y, 2));
			dnorm = distance/dmax;
			image.putpixel((x,y), (int(255 - dnorm*255.0), int(255- dnorm*255.0), int(255 - dnorm*255.0)));
	return image;

def genPlasma(width, height):
	image = Image.new("RGB", (width, height), "black")
	
	a = random.random();
	b = random.random();
	c = random.random();
	d = random.random();
	
	return image;

#--------------COMMAND FUNCTIONS--------------

def mandlebrot(max_iteration, size):
	width = 32*size;
	height = 32*size;
	
	img = genMandlebrot(width, height, max_iteration, Point(128, 0));
	return img



def genDistance(size, x, y):
	width = 512*size;
	height = 512*size;
	
	img = distanceImg(width, height, Point(x, y));
	img.save("distance.png")

def genSeries():
	width = 128*4;
	height = 128*4;
	images = []
	for index in range(height/2):
		img = genMandlebrot(width, height, 1, Point(128, index*2))
		#img = distanceImg(width, height, Point(128/2, index));
		img.save("Fractal\distance"+str(index)+".png")
	#images2gif.writeGif("reverse.gif", images, duration=10.0);
	#
#--------------TEST CASES--------------

def testPointConvert():
	width = 400;
	height = 500;
	point = Point(int(width/3), int(height/3));
	point.echo();
	point = convertCord(point, width, height);
	point.echo();

def testPointClass():
	point = Point();
	point.echo();
	print(point.get());
	x, y = point.get();
	print(x);
	print(y);
