import os, sys
import datetime

TIME_STAMP_FORMAT = "%d-%m-%y %H:%M:%S"
DEFAULT_LEVEL_MAP = {
	"CRIT": ["CRIT"],
	"INFO": ["CRIT", "INFO"],
	"DEBUG": ["CRIT", "INFO", "DEBUG"]
}

class Logger():
	def __init__(self, log_level, log_path, log_file):
		self.log_path = log_path
		self.log_file = log_file
		self.log_level_set = self._init_log_levels(log_level)

	def _init_log_levels(self, log_level):
		return DEFAULT_LEVEL_MAP[log_level]

	#####################
	# UTILITY FUNCTIONS #
	#####################
	def _open_logfile(self):
		log_file_path = '/'.join([self.log_path, self.log_file])
		file = open(log_file_path, 'a')
		return file

	def enabled(self, log_level):
		if log_level in self.log_level_set:
			return True
		return False

	##################
	# CALL FUNCTIONS #
	##################
	def log(self, level, message):
		if self.enabled(level):
			logfile = self._open_logfile()
			time_now = datetime.datetime.now()
			timestamp = time_now.strftime(TIME_STAMP_FORMAT)
			logstring = "{TIMESTAMP} {LOGLEVEL} {MESSAGE}\n".format(
				TIMESTAMP = timestamp,
				LOGLEVEL = level,
				MESSAGE = str(message)
			)
			logfile.write(logstring)
			logfile.close()

if __name__ == "__main__":
	#log_level, log_path, log_file
	logger = Logger("CRIT", os.getcwd(), "test.log")
	logger.log('CRIT', 'OK - Logging string')
	logger.log('INFO', 'ERROR - Shouldnt be displayed')
	logger.log('CRIT', str(logger.enabled('TEST')))
