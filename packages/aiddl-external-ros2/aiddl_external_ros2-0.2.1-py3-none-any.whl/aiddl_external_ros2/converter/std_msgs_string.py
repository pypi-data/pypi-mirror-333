from aiddl_core.representation import Str


class StringConverter:
    @staticmethod
    def ros2aiddl(string_msg):
        return Str(string_msg)

    @staticmethod
    def aiddl2ros(string):
        return string.string
