import tornado.ioloop
import tornado.web

import os, sys

import PIL
import simplejson as json

sys.path.append("./lib")
from handlers import RequestHandler
from utils import logger

def main():
	LOG_MIN_LEVEL = "CRIT"
	LOG_PATH = "{}/logs".format(os.getcwd())
	LOG_NAME = "frakserv.log"

	app_logger = logger.Logger(LOG_MIN_LEVEL, LOG_PATH, LOG_NAME)
	app_logger.log("INFO", "Logger initialized")

	application = tornado.web.Application([
		(r"/", RequestHandler.MainHandler, dict(
			logger = app_logger
		)),
	])
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
	app_logger.log("CRIT", "Server started")

if __name__ == "__main__":
	main()
