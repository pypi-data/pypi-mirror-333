from aiddl_core.representation import Real


class Float64Converter:
    @staticmethod
    def ros2aiddl(float64_msg):
        return Real(float64_msg)

    @staticmethod
    def aiddl2ros(real_term: Real):
        return real_term.unpack()
