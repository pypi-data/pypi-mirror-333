import os
from .base import MarkerBase


class MarkerEnvBase(MarkerBase):

    def execute(self, context, command, marker_node, marker_set):
        argv = self.split_raw(command, 2)[1:]
        environ = self.get_environ(context)
        if len(argv) == 1:
            environ.pop(argv[0], None)
        elif len(argv) == 2:
            environ[argv[0]] = str(argv[1])
        else:
            environ.clear()

    def get_environ(self, context):
        raise NotImplementedError


class EnvMarker(MarkerEnvBase):
    tag_head = "env"

    def get_environ(self, context):
        return os.environ


class EnvShellMarker(MarkerEnvBase):
    tag_head = "envs"

    def get_environ(self, context):
        return context.environ.data
