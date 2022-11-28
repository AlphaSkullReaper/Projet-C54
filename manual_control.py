from niveau1 import FiniteStateMachine


class ledBlinkers:
    def __init__(self):
        pass


class eyesBlinkers:
    def __init__(self):
        pass


class GoPiGo3:
    def __init__(self):
        pass


class Robot:
    def __init__(self, robot: 'GoPiGo3', led_blinkers: 'ledBlinkers', eye_blinkers: 'eyesBlinkers'):
        self.robot = robot
        self.led_blinkers = led_blinkers
        self.eye_blinkers = eye_blinkers

    def start(self):
        pass


class C64Project(FiniteStateMachine):
    def __init__(self, robot: Robot):
        self.robot = robot
        layout = FiniteStateMachine.Layout()

        # layout.initial_state = self.__off
        # layout.add_state(self.__off)

        super().__init__(layout)

    def start(self) -> None:
        self.robot.start()
