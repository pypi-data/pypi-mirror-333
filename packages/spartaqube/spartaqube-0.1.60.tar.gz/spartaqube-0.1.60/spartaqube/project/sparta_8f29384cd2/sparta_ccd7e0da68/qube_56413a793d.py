_A='windows'
import os,platform,getpass
def sparta_5618ce909a():
	try:A=str(os.environ.get('IS_REMOTE_SPARTAQUBE_CONTAINER','False'))=='True'
	except:A=False
	return A
def sparta_4b0fbcb7ae():
	A=platform.system()
	if A=='Windows':return _A
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
def sparta_21526a056d():
	if sparta_5618ce909a():return'/spartaqube'
	A=sparta_4b0fbcb7ae()
	if A==_A:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube"
	elif A=='linux':B=os.path.expanduser('~/SpartaQube')
	elif A=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube')
	return B