from aiddl_core.representation import Real


class FloatConverter:
    @staticmethod
    def ros2aiddl(msg):
        return Real(msg)

    @staticmethod
    def aiddl2ros(real_term: Real):
        return real_term.unpack()
