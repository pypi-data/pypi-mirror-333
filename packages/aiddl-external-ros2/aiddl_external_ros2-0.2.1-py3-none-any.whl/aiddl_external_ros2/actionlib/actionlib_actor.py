from __future__ import print_function

from aiddl_external_grpc_python.actor import ActorServer
import aiddl_external_grpc_python.generated.actor_pb2 as actor_pb2
import aiddl_external_grpc_python.generated.aiddl_pb2 as aiddl_pb2

from actionlib_msgs.msg import GoalStatus

class ActionlibActorServer(ActorServer):
    def __init__(self,
                 port,
                 topic,
                 ros_action_lib_client,
                 f_is_supported,
                 f_extract_goal,
                 f_extract_fb=None):
        super(ActionlibActorServer, self).__init__(port)
        self.current_id = 0
        self.topic = topic
        self.client = ros_action_lib_client
        self.ros_goal_future = None
        self.status_history = {}
        self.f_is_supported = f_is_supported
        self.f_extract_goal = f_extract_goal
        self.f_extract_fb = f_extract_fb
        self.feedback = None
        
    def _feedback_handler(self, fb):
        print("Handling feedback...")
        if self.f_extract_fb is None:
            return None
        self.feedback = self.f_extract_fb(fb)
        
        
    def IsSupported(self, request, context):
        is_supported = self.f_is_supported(request)
        print('Is %s supported? %s' % (str(request), str(is_supported)))
        r = actor_pb2.Supported(is_supported=is_supported)
        print('Response:', r)
        return r
               
    def Dispatch(self, request, context):
        self.current_id += 1
        self.client.wait_for_server()
        goal = self.f_extract_goal(request)
        self.ros_goal_future = self.client.send_goal_async(goal, self._feedback_handler)
        return self.currentGoalToStatus()

    def Status(self, request, context):
        return self.currentGoalToStatus()

    def Cancel(self, request, context):
        return actor_pb2.Status(
            id=self.next_id,
            status=2,
            feedback=aiddl_pb2.AiddlStr(""),
            msg=""
        )

    def currentGoalToStatus(self):
        pb_status = None
        status = self.client.get_state()

        if status == GoalStatus.PENDING:
            pb_status = actor_pb2.PENDING
        elif status == GoalStatus.ACTIVE:
            pb_status = actor_pb2.ACTIVE
        elif status == GoalStatus.PREEMPTED:
            pb_status = actor_pb2.PREEMPTED
        elif status == GoalStatus.SUCCEEDED:
            pb_status = actor_pb2.SUCCEEDED
        elif status == GoalStatus.ABORTED:
            pb_status = actor_pb2.ERROR
        elif status == GoalStatus.REJECTED:
            pb_status = actor_pb2.REJECTED
        elif status == GoalStatus.PREEMPTING:
            pb_status = actor_pb2.PREEMPTING
        elif status == GoalStatus.RECALLING:
            pb_status = actor_pb2.RECALLING
        elif status == GoalStatus.RECALLED:
            pb_status = actor_pb2.RECALLED
        else:
            pb_status = actor_pb2.ERROR
            print("Unknown status:", status)

        feedback = ""
        if self.feedback is not None:
            feedback = str(self.feedback)
            
        r = actor_pb2.Status(
            id=self.current_id,
            state=pb_status,
            feedback=aiddl_pb2.AiddlStr(aiddl_str=feedback),
            msg=""
        )
        self.status_history[self.current_id] = r
        return r
