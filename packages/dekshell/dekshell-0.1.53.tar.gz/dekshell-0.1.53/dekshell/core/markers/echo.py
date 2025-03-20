import sys
from .base import MarkerBase


class EchoMarker(MarkerBase):
    tag_head = "echo"

    def execute(self, context, command, marker_node, marker_set):
        sys.stdout.write(self.split_raw(command, 1, self.tag_head)[-1] + '\n')


class ErrorEchoMarker(MarkerBase):
    tag_head = "echo!"

    def execute(self, context, command, marker_node, marker_set):
        sys.stderr.write(self.split_raw(command, 1, self.tag_head)[-1] + '\n')
