import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_22da4d4238.sparta_8549dc3b58 import qube_e76a8b5516,qube_9f4ec8611f,qube_145cea1aed,qube_3dd85ea033,qube_761093dddb,qube_7d4e17aa01,qube_5a99a3c5a2,qube_e14aa4db9d,qube_cf3b433a4f
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
def sparta_c189582806(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_c189582806(qube_e76a8b5516.StatusWS)),url('ws/notebookWS',sparta_c189582806(qube_9f4ec8611f.NotebookWS)),url('ws/wssConnectorWS',sparta_c189582806(qube_145cea1aed.WssConnectorWS)),url('ws/pipInstallWS',sparta_c189582806(qube_3dd85ea033.PipInstallWS)),url('ws/gitNotebookWS',sparta_c189582806(qube_761093dddb.GitNotebookWS)),url('ws/xtermGitWS',sparta_c189582806(qube_7d4e17aa01.XtermGitWS)),url('ws/hotReloadLivePreviewWS',sparta_c189582806(qube_5a99a3c5a2.HotReloadLivePreviewWS)),url('ws/apiWebserviceWS',sparta_c189582806(qube_e14aa4db9d.ApiWebserviceWS)),url('ws/apiWebsocketWS',sparta_c189582806(qube_cf3b433a4f.ApiWebsocketWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)