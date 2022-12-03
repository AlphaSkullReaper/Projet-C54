from Last_Jupyter_Version import RobotState,Robot,SideBlinkers,Blinker,EyeBlinkers,LedBlinkers
from niveau2 import MonitoredState
from niveau1 import State, FiniteStateMachine
from niveau2 import ConditionalTransition, Condition, StateValueCondition




class RemoteControlTransition(ConditionalTransition):
    def __init__(self, condition: 'Condition' = None, next_state: 'RobotState' = None, remote_control: 'RemoteControl' = None):
        super().__init__(next_state, condition)
        self._remote_control = remote_control
        #todo: bouncing

class RemoteValueCondition(Condition):
    def __init__(self,expected_value:str,remote_control: 'RemoteControl' = None, inverse:bool = False):
        self._remote_control = remote_control
        self.__keycodes = ['', 'up', 'left', 'ok', 'right', 'down', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']
        if expected_value in self.__keycodes :
            self.__expected_value = expected_value
        else:
            raise  Exception("Expected value must be a valid keycode")
        super().__init__(inverse)

    def _compare(self) -> bool:
        return self._remote_control.get_remote_code() == self.__expected_value

    @property
    def expected_value(self) -> str:
        return self.__expected_value

    @expected_value.setter
    def expected_value(self, new_expected_value: str):
        if new_expected_value in self.__keycodes :
            self.__expected_value = new_expected_value
        else:
            raise  Exception("Expected value must be a valid keycode")


class ManualControl(RobotState):
    class StopState(RobotState):
        def __init__(self, parameters: 'State.Parameters' = State.Parameters() ):
            super().__init__(parameters)
            self.custom_value = 'stop'

        def _do_entering_action(self) -> None:
            self._robot.stop()
            self._robot.led_close()

    class RotateRightState(RobotState):
        def __init__(self, parameters: 'State.Parameters' = State.Parameters() ):
            super().__init__(parameters)
            self.custom_value = 'right'

        def _do_entering_action(self) -> None:
            self._robot.right()
            self._robot.led_blinkers.blink1(SideBlinkers.Side.RIGHT, 1.0, 0.50)

    class RotateLeftState(RobotState):
        def __init__(self, parameters: 'State.Parameters' = State.Parameters() ):
            super().__init__(parameters)
            self.custom_value = 'left'

        def _do_entering_action(self) -> None:
            self._robot.left()
            self._robot.led_blinkers.blink1(SideBlinkers.Side.LEFT, 1.0, 0.50)

    class ForwardState(RobotState):
        def __init__(self,parameters: 'State.Parameters' = State.Parameters() ):
            super().__init__(parameters)
            self.custom_value = 'forward'

        def _do_entering_action(self) -> None:
            self._robot.forward()
            self._robot.led_blinkers.blink1(SideBlinkers.Side.BOTH,1.0,0.25)

    class BackwardState(RobotState):
        def __init__(self, parameters: 'State.Parameters' = State.Parameters() ):
            super().__init__(parameters)
            self.custom_value = 'Backward'

        def _do_entering_action(self) -> None:
            self._robot.backward()
            self._robot.led_blinkers.blink1(SideBlinkers.Side.BOTH, 1.0, 0.75)

    def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
        super().__init__(robot, parameters)
        rotate_left = self.RotateLeftState()
        forward = self.ForwardState()
        stop = self.StopState()
        rotate_right = self.RotateRightState()
        backwards = self.BackwardState()

        rc= None #todo: intitialisation

        left_condition = RemoteValueCondition('left',rc)
        left_transition = RemoteControlTransition(left_condition,rotate_left,rc)
        stop.add_transition(left_transition)

        not_left_condition = RemoteValueCondition('', rc)
        left_transition = RemoteControlTransition(not_left_condition, stop, rc)
        rotate_left.add_transition(left_transition)

        down_condition = RemoteValueCondition( 'down', rc)
        down_transition = RemoteControlTransition(down_condition, backwards, rc)
        stop.add_transition(down_transition)

        not_down_condition = RemoteValueCondition('', rc)
        not_down_transition = RemoteControlTransition(not_down_condition, stop, rc)
        backwards.add_transition(not_down_transition)

        right_condition = RemoteValueCondition('right', rc)
        right_transition = RemoteControlTransition(right_condition, rotate_right, rc)
        stop.add_transition(right_transition)

        not_right_condition = RemoteValueCondition('', rc)
        not_right_transition = RemoteControlTransition(not_right_condition, stop, rc)
        backwards.add_transition(not_right_transition)

        forward_condition = RemoteValueCondition('right', rc)
        forward_transition = RemoteControlTransition(forward_condition, forward, rc)
        stop.add_transition(forward_transition)

        not_forward_condition = RemoteValueCondition('', rc)
        not_forward_transition = RemoteControlTransition(not_forward_condition, stop, rc)
        backwards.add_transition(not_forward_transition)
        self.__layout =FiniteStateMachine.Layout()
        self.__layout.initial_state = stop
        self.__layout.add_states([stop,rotate_left,rotate_right,forward,backwards])

        self.Fsm =FiniteStateMachine(self.__layout)

    def track(self) -> None:
        self._robot.led_blinkers.track()
        return self.Fsm.track()
















