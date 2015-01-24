
class ImcInterfaceResponse:
    def __init__(self, status, error=None, message_type=None, message_params=None ):
        self.status=status
        self.error=error
        self.message_type=message_type
        self.message_params=message_params
        self._msgoriginated=[]

    def add_msg_originated(self, msg, index=0):
        array_position=index if index else len(self._msgoriginated)
        self._msgoriginated.insert(array_position,msg)

    def get_msg_originated(self):
        return self._msgoriginated
