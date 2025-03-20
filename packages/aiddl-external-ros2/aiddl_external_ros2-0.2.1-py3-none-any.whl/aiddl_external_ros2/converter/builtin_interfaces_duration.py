from aiddl_core.representation import Real, Tuple, Int, Term, List, KeyVal
from builtin_interfaces.msg import Duration

from aiddl_external_ros2.converter.constant import SECS, NSECS


class DurationConverter:
    @staticmethod
    def ros2aiddl(msg: Duration):
        return List(
            KeyVal(SECS, Int(msg.sec)),
            KeyVal(NSECS, Int(msg.nanosec)))

    @staticmethod
    def aiddl2ros(duration_term: Term):
        msg = Duration()
        msg.sec = duration_term[SECS].unpack()
        msg.nanosec = duration_term[NSECS].unpack()
        return msg
