from .base import MarkerBase, MarkerWithEnd, cmd_call_prefix
from .empty import EmptyMarker


class ExecMarker(MarkerBase):
    tag_head = '='

    def execute(self, context, command, marker_node, marker_set):
        args = self.split_raw(command, 1, self.tag_head)
        if args[1]:
            self.eval(context, args[1])


class ExecLinesMarker(MarkerWithEnd):
    tag_head = '=='

    def execute(self, context, command, marker_node, marker_set):
        code = self.get_inner_content(context, marker_node)
        self.eval_lines(context, code)
        return []


class ExecLinesUpdateMarker(MarkerWithEnd):
    tag_head = '==='

    def execute(self, context, command, marker_node, marker_set):
        code = self.get_inner_content(context, marker_node)
        context.update_variables(self.eval_lines(context, code))
        return []


class ExecCmdCallMarker(MarkerBase):
    tag_head = cmd_call_prefix

    def execute(self, context, command, marker_node, marker_set):
        self.cmd_call(context, command.split(self.tag_head, 1)[-1].strip())


class ExecCmdCallLinesMarker(MarkerWithEnd):
    tag_head = f'{cmd_call_prefix}{cmd_call_prefix}'
    cmd_call_marker_cls = ExecCmdCallMarker
    targets_marker_cls = (EmptyMarker,)

    def execute(self, context, command, marker_node, marker_set):
        marker = marker_set.find_marker_by_cls(self.cmd_call_marker_cls)
        result = []
        for child in marker_node.children:
            if child.is_type(*self.targets_marker_cls):
                node = marker_set.node_cls(
                    marker,
                    self.cmd_call_marker_cls.tag_head + ' ' + child.command,
                    child.index,
                    marker_node,
                    child.command
                )
                result.append(node)
            else:
                result.append(child)
        return result
