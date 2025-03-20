from .base import MarkerBase


class DefaultMarker(MarkerBase):
    tag_head = "default"

    def execute(self, context, command, marker_node, marker_set):
        args = self.split_raw(command, 2)
        var_name = self.get_item(args, 1)
        try:
            self.eval(context, var_name)
        except NameError:
            self.set_var(context, args, 1, self.eval(context, args[2]))
