class ActionConverter(object):
    def __init__(self, msg_class_str, request, feedback, result):
        self._msg_class = load_class_from_string(msg_class_str)
        self._request = []
        for avp in request.split(","):
            att_val = avt.split(":")
            field = att_val[0]
            msg_class = load_class_from_string(att_val[1])
            self._request.append((field, msg_class))

        self._feedback = feedback
        self._result = result


    def request_aiddl2ros(self, term):
        msg = self._msg_class.Request()



        pass

    def feedback_ros2aiddl(self, msg):
        pass

    def result_ros2aiddl(self, msg):
        pass