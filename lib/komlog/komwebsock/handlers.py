import asyncio
import uuid
import json
from tornado import websocket
from komlog.komfig import logging
from komlog.komwebsock import auth
from komlog.komimc import api as msgapi
from komlog.komlibs.interface.websocket import session
from komlog.komlibs.interface.websocket import api as wsapi

class WSConnectionHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    @auth.agent_authenticated
    def open(self):
        session.set_session(passport=self.passport, callback=self.agent_callback)

    @auth.agent_authenticated
    def on_message(self, message):
        try:
            message=json.loads(message)
        except Exception:
            self.close()
        else:
            result=wsapi.process_message(passport=self.passport, message=message)
            asyncio.ensure_future(msgapi.send_messages(result.imc_messages))
            for msg in result.ws_messages:
                self.write_message(json.dumps(msg.to_dict()))

    def on_connection_close(self):
        psp = getattr(self, 'passport', None)
        if psp:
            session.unset_session(passport=psp)

    @auth.agent_active
    def agent_callback(self, message):
        self.write_message(json.dumps(message))

HANDLERS = [
    (r'/', WSConnectionHandler),
]


