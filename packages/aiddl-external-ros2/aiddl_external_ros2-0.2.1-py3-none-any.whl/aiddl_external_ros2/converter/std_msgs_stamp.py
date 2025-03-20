from aiddl_core.representation import Int
from aiddl_core.representation import List
from aiddl_core.representation import KeyVal
from aiddl_external_ros2.converter.constant import SECS, NSECS

from builtin_interfaces.msg import Time

import rclpy

class StampConverter:
    @staticmethod
    def ros2aiddl(stamp_msg):
        return List(
            KeyVal(SECS, Int(stamp_msg.sec)),
            KeyVal(NSECS, Int(stamp_msg.nanosec)))

    @staticmethod
    def aiddl2ros(stamp):
        msg = Time()
        msg.sec = stamp[SECS].unpack()
        msg.nanosec = stamp[NSECS].unpack()
        return msg
