import threading

from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


@has_log
class Ldens3300StreamInterface(StreamInterface):
    commands = {}
    in_terminator = ""
    out_terminator = "\r\n"

    def __init__(self) -> None:
        super(Ldens3300StreamInterface, self).__init__()
        self._queue_next_unsolicited_message()

    def _queue_next_unsolicited_message(self) -> None:
        timer = threading.Timer(1.0, self.get_data_unsolicited)
        timer.daemon = True
        timer.start()

    def handle_error(self, request: str, error: str) -> None:
        print("An error occurred at request " + repr(request) + ": " + repr(error))

    @if_connected
    def unsolicited_reply(self, handler: str) -> None:
         handler.unsolicited_reply(
            f"T= {self.device.temperature} <°C> D= {self.device.density} <kg/m³>"
        )

    def get_data_unsolicited(self) -> None:
        self._queue_next_unsolicited_message()

        try:
            handler = self.handler
        except AttributeError:
            # Happens if no client is currently connected.
            return
        else:
            self.unsolicited_reply(handler)
