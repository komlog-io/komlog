import uuid
import json
from tornado import websocket
from komfig import logger
from komwebsock import auth
from komlibs.interface.websocket import api as wsapi

class WAConnectionHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    #@auth.agent_authenticated
    def open(self):
        self.username='jcazor' #esto hay que cambiarlo al implementar autenticacion
        self.aid='7c3cd617f6be4dfcbf18a85dbcb86fde' #esto hay que cambiarlo al implementar autenticacion

    #@auth.agent_authenticated
    def on_message(self, message):
        try:
            message=json.loads(message)
        except (TypeError, json.decoder.JSONDecodeError):
            self.close()
        else:
            response=wsapi.process_message(username=self.username, aid=self.aid, message=message)
            self.write_message(json.dumps({'status':response.status,'reason':response.reason,'error':response.error}))

    #@auth.agent_authenticated
    def on_close(self):
        logger.logger.debug('session closed')

HANDLERS = [
            (r'/ws/?', WAConnectionHandler),
            ]


