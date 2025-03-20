from nav_msgs.srv import GetMap

from aiddl_external_ros2.converter.msg.nav.nav_msgs_occupancy_grid import occupancy_grid_2_aiddl

class GetMapConverter(object):
    @staticmethod
    def request_aiddl2ros(term):
        return GetMap.Request()

    @staticmethod
    def result_ros2aiddl(msg):
        return occupancy_grid_2_aiddl(msg)
