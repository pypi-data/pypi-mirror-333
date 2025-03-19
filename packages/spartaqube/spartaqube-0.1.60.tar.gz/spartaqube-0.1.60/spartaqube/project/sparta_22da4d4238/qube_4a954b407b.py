import time
from project.logger_config import logger
def sparta_2fd27dc92f():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_2fd27dc92f()
def sparta_9128e04559(tempBool=True):
	A=next(TicToc)
	if tempBool:logger.debug('Elapsed time: %f seconds.\n'%A);return A
def sparta_9b4399265b():sparta_9128e04559(False)