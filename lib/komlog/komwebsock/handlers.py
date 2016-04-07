import uuid
import json
from tornado import websocket
from komlog.komfig import logging
from komlog.komwebsock import auth
from komlog.komlibs.interface.websocket import api as wsapi

class WSConnectionHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        pass

    @auth.agent_authenticated
    def on_message(self, message):
        try:
            message=json.loads(message)
        except Exception:
            self.close()
        else:
            response=wsapi.process_message(passport=self.passport, message=message)
            self.write_message(json.dumps({'status':response.status,'reason':response.reason,'error':response.error}))

    def on_close(self):
        logging.logger.debug('session closed')

HANDLERS = [
            (r'/', WSConnectionHandler),
            ]


