import json,base64,asyncio,subprocess,uuid,os,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_8f29384cd2.sparta_63edf7d78c import qube_5af9e48ff5 as qube_5af9e48ff5
from project.sparta_8f29384cd2.sparta_99ae4fa4f2 import qube_663812ae0c
from project.sparta_8f29384cd2.sparta_a6d0a04f89 import qube_684e4bab71 as qube_684e4bab71
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.qube_7503c9ec03 import Connector as Connector
from project.logger_config import logger
def sparta_b2ac8ba7a3(json_data,user_obj):
	D='key';A=json_data;logger.debug('Call autocompelte api');logger.debug(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_3f51e6cff5(B)
	return{'res':1,'output':C,D:B}
def sparta_3f51e6cff5(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";H={'http':os.environ.get('http_proxy',None),'https':os.environ.get('https_proxy',None)};C=requests.get(G,proxies=H)
	try:
		if int(C.status_code)==200:
			I=json.loads(C.text);D=I['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]