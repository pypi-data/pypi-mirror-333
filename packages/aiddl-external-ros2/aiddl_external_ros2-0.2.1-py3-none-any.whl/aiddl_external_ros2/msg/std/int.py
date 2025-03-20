class IntConverter:
    @staticmethod
    def ros2aiddl(msg):
        return Int(msg)

    @staticmethod
    def aiddl2ros(term):
        return int(term.unpack())