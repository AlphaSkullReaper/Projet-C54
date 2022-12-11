from niveau1 import State, FiniteStateMachine
from niveau2 import RobotState, MonitoredState, RemoteValueCondition, RemoteControlTransition
from niveau3 import SideBlinkers


class LedBlinkers(SideBlinkers):
    def __init__(self, robot):
        self.__robot = robot
        super().__init__(lambda: LedBlinkers.LedOffLeftState(self.__robot),
                         lambda: LedBlinkers.LedOnLeftState(self.__robot),
                         lambda: LedBlinkers.LedOffRightState(self.__robot),
                         lambda: LedBlinkers.LedOnRightState(self.__robot))

    class LedOnLeftState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)  # TODO:validation
            self.custom_value = True

        def _do_entering_action(self) -> None:
            self._robot.led_on(1)

    class LedOffLeftState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)  # TODO:validation
            self.custom_value = False

        def _do_entering_action(self) -> None:
            self._robot.led_off(1)

    class LedOnRightState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)  # TODO:validation
            self.custom_value = True

        def _do_entering_action(self) -> None:
            self._robot.led_on(0)

    class LedOffRightState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)  # TODO:validation
            self.custom_value = False

        def _do_entering_action(self) -> None:
            self._robot.led_off(0)


class EyeBlinkers(SideBlinkers):
    def __init__(self, a_robot):
        self._robot = a_robot  # TODO:validation
        super().__init__(lambda: EyeBlinkers.EyeOffLeftState(self._robot),
                         lambda: EyeBlinkers.EyeOnLeftState(self._robot),
                         lambda: EyeBlinkers.EyeOffRightState(self._robot),
                         lambda: EyeBlinkers.EyeOnRightState(self._robot))

    class EyeOnLeftState(RobotState):
        def __init__(self, a_robot, parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)  # TODO:validation
            self.custom_value = True
            self.couleur = (255, 0, 0)

        def _do_entering_action(self) -> None:
            self._robot.open_left_eye()

    class EyeOffLeftState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)
            self.custom_value = False  # TODO:validation
            self.couleur = (255, 0, 0)

        def _do_entering_action(self) -> None:
            self._robot.close_left_eye()

    class EyeOnRightState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)  # TODO:validation
            self.custom_value = True
            self.couleur = (255, 0, 0)

        def _do_entering_action(self) -> None:
            self._robot.open_right_eye()

    class EyeOffRightState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)
            self.custom_value = False  # TODO:validation
            self.couleur = (255, 0, 0)

        def _do_entering_action(self) -> None:
            self._robot.close_right_eye()


class Robot:
    def __init__(self):
        self.__robot: 'easy.EasyGoPiGo3' = easy.EasyGoPiGo3()
        self.__led_blinkers: 'LedBlinkers' = LedBlinkers(self.__robot)
        self.__eyes_blinkers: 'EyeBlinkers' = EyeBlinkers(self.__robot)

    @property
    def led_blinkers(self) -> 'LedBlinkers':
        return self.__led_blinkers

    @property
    def eye_blinkers(self) -> 'EyeBlinkers':
        return self.__eyes_blinkers

    def change_couleur(self, couleur: tuple, side: SideBlinkers.Side):
        if side == SideBlinkers.Side.LEFT:
            self.set_left_eye_color(couleur)  # TODO:validation
            self.open_left_eye()
        elif side == SideBlinkers.Side.RIGHT:
            self.set_right_eye_color(couleur)
            self.open_right_eye()
        elif side == SideBlinkers.Side.BOTH:
            self.set_eye_color(couleur)
            self.open_eyes()

    def shut_down(self) -> None:
        self.__led_blinkers.stop()
        self.__eyes_blinkers.stop()
        self.stop()
        self.close_eyes()

    def led_close(self) -> None:
        self.__robot.led_off(0)
        self.__robot.led_off(1)

    def set_seed(self, in_speed: int) -> None:
        self.__robot.set_speed(in_speed)

    def get_speed(self) -> int:
        return self.__robot.get_speed()

    def reset_seed(self) -> None:
        self.__robot.reset_speed()

    def stop(self) -> None:
        self.__robot.stop()

    def foward(self) -> None:
        self.__robot.forward()

    def drive_cm(self, dist: float, blocking: bool = True) -> None:  # TODO:validation
        self.__robot.drive_cm(dist, blocking)

    def drive_inches(self, dist: float, blocking: bool = True) -> None:  # TODO:validation
        self.__robot.drive_inches(dist, blocking)

    def drive_degrees(self, degrees: float, blocking: bool = True):  # TODO: Check return without follow up
        return self.__robot.drive_degrees(degrees, blocking)  # TODO:validation

    def backward(self) -> None:
        self.__robot.backward()

    def right(self) -> None:
        self.__robot.right()

    def spin_right(self) -> None:
        self.__robot.spin_right()

    def left(self) -> None:
        self.__robot.left()

    def spin_left(self) -> None:
        self.__robot.spin_left()

    def steer(self, left_percent: int, right_percent: int) -> None:
        self.__robot.steer(left_percent, right_percent)  # TODO:validation

    def orbit(self, degrees: int, radius_cm: int = 0, blocking: bool = True):  # TODO: Check return without follow up
        return self.__robot.orbit(degrees, radius_cm, blocking)  # TODO:validation

    def target_reached(self, left_target_degrees: int, right_target_degrees: int) -> bool:
        return self.__robot.target_reached(left_target_degrees, right_target_degrees)  # TODO:validation

    def reset_encoders(self, blocking: bool = True) -> None:
        return self.__robot.reset_encoders(blocking)  # TODO:validation

    def read_encoders_average(self, units: str = "cm") -> float:
        return self.robot.read_encoders_average(units)  # TODO:validation

    def turn_degrees(self, degrees: int, blocking: bool = True) -> None:
        self.turn_degrees(degrees, blocking)  # TODO:validation

    def blinker_on(self, id: int) -> None:
        self.__robot.blinker_on(id)  # TODO:validation

    def blinker_off(self, id: int) -> None:
        self.__robot.blinker_off(id)  # TODO:validation

    def lef_on(self, id: int) -> None:
        self.__robot.led_on(id)  # TODO:validation

    def lef_off(self, id: int) -> None:
        self.__robot.led_off(id)  # TODO:validation

    def set_left_eye_color(self, color: tuple) -> None:
        self.__robot.set_left_eye_color(color)  # TODO:validation

    def set_right_eye_color(self, color: tuple) -> None:
        self.__robot.set_right_eye_color(color)  # TODO:validation

    def set_eye_color(self, color: tuple) -> None:
        self.__robot.set_eye_color(color)  # TODO:validation

    def open_left_eye(self) -> None:
        self.__robot.open_left_eye()

    def open_right_eye(self) -> None:
        self.__robot.open_right_eye()

    def open_eyes(self) -> None:
        self.__robot.open_eyes()

    def close_left_eye(self) -> None:
        self.__robot.close_left_eye()

    def close_right_eye(self) -> None:
        self.__robot.close_right_eye()

    def close_eyes(self) -> None:
        self.__robot.close_eyes()

    def init_light_sensor(self, port: str = "AD1"):  # TODO check return easysensors.LightSensor
        return self.__robot.init_light_sensor(port)  # TODO:validation

    def init_sound_sensor(self, port: str = "AD1"):  # TODO easysensors.SoundSensor
        return self.__robot.init_sound_sensor(port)  # TODO:validation

    def init_loudness_sensor(self, port: str = "AD1"):
        return self.__robot.init_loudness_sensor(port)  # TODO:validation

    def init_ultrasonic_sensor(self, port: str = "AD1"):
        return self.__robot.init_ultrasonic_sensor(port)  # TODO:validation

    def init_buzzer(self, port: str = "AD1"):
        return self.__robot.init_buzzer(port)  # TODO:validation

    def init_led(self, port: str = "AD2"):
        return self.__robot.init_led(port)  # TODO:validation

    def init_button_sensor(self, port: str = "AD1"):
        return self.__robot.init_button_sensor(port)  # TODO:validation

    def init_line_follower(self, port: str = "I2C"):
        return self.__robot.init_line_follower(port)  # TODO:validation

    def init_servo(self, port: str = "SERVO1"):
        return self.__robot.init_servo(port)  # TODO:validation

    def init_distance_sensor(self, port: str = "I2C"):
        return self.__robot.init_distance_sensor(port)  # TODO:validation

    def init_light_color_sensor(self, port: str = "I2C", led_state=True):
        return self.__robot.init_light_color_sensor(port)  # TODO:validation

    def init_imu_sensor(self, port: str = "I2C"):
        return self.__robot.init_imu_sensor(port)  # TODO:validation

    def init_dht_sensor(self, sensor_type: int = 0):
        return self.__robot.init_dht_sensor(sensor_type)  # TODO:validation

    def init_remote(self, port: str = "AD1"):
        return self.__robot.init_remote(port)  # TODO:validation

    def init_motion_sensor(self, port: str = "AD1"):
        return self.__robot.init_motion_sensor(port)


class C64Project(FiniteStateMachine):
    def __init__(self):
        self._robot = Robot()
        self._remote_control = self._robot.init_remote()

        layout = FiniteStateMachine.Layout()
        terminal_state_parameters = State.Parameters(False, False, True)

        self.__robot_instantiation = RobotState(self._robot)
        self.__robot_instantiation.add_entering_action(lambda: self.__instantiation_check())

        self.__instantiation_failed = MonitoredState()
        self.__instantiation_failed.add_entering_action(lambda: print("An error has occured : "
                                                                      "Instantiation failed. Shutting down."))
        self.__end = MonitoredState(terminal_state_parameters)
        self.__end.add_entering_action(lambda: print("Final message. Good bye good Sir (of Lady)!"))

        self.__home = RobotState(self._robot)

        self.__robot_integrity = RobotState(self._robot)
        self.__robot_integrity.add_entering_action(lambda: self.__integrity_check())

        self.__integrity_failed = RobotState(self._robot)
        self.__integrity_failed.add_entering_action(lambda: self.__integrity_failed_entering_action())

        self.__integrity_succeeded = RobotState(self._robot)
        self.__integrity_succeeded.add_entering_action(lambda: self.__integrity_succeeded_entering_action())

        self.__shut_down_robot = RobotState(self._robot)
        self.__shut_down_robot.add_entering_action(lambda: self.__shutdown_robot_entering_action())

        self.__instantiation_failed.add_entering_action(lambda: print("instantiation failed"))
        self.__end.add_entering_action(lambda: print("Final message. End."))

        self._orange_link(self.__robot_instantiation, self.__robot_integrity, True)

        self._orange_link(self.__robot_instantiation, self.__instantiation_failed, False)

        self._orange_link(self.__robot_integrity, self.__integrity_succeeded, True)
        self._orange_link(self.__robot_integrity, self.__integrity_failed, False)

        self._blue_link(self.__instantiation_failed, self.__end)
        self._green_link(self.__instantiation_failed, self.__shut_down_robot, 5.0)
        self._green_link(self.__shut_down_robot, self.__end, 3.0)
        self._green_link(self.__integrity_succeeded, self.__home, 3.0)

        self.__task1 = ManualControl(self._remote_control, self._robot)
        self._purple_link('1', self.__home, self.__task1, self._remote_control)
        self._purple_link('ok', self.__task1, self.__home, self._remote_control)

        layout.add_state(self.__robot_instantiation)
        layout.add_state(self.__instantiation_failed)
        layout.add_state(self.__end)
        layout.add_state(self.__home)
        layout.add_state(self.__robot_integrity)
        layout.add_state(self.__integrity_failed)
        layout.add_state(self.__integrity_succeeded)
        layout.add_state(self.__shut_down_robot)
        layout.initial_state = self.__robot_instantiation
        super().__init__(layout)

    def __instantiation_check(self) -> None:
        self.__robot_instantiation.custom_value = self._robot is not None and isinstance(self._robot, Robot)

    def __integrity_check(self) -> None:
        try:
            if self._remote_control is None:
                self._remote_control = self._robot.init_remote()
            self._robot.init_led()
            self._robot.init_servo()
            self._robot.init_distance_sensor()
            self.__robot_integrity.custom_value = True
        except:
            print("Exception on integrety check")
            self.__robot_integrity.custom_value = False

    def __integrity_failed_entering_action(self) -> None:
        print("An error has occured: Integration failed, Instantiation failed. Shutting down.")
        self._robot.change_couleur((255, 0, 0), SideBlinkers.Side.BOTH)
        self._robot.eye_blinkers.blink2(side=SideBlinkers.Side.BOTH, cycle_duration=0.5,
                                        total_duration=5.0, end_off=False)

    def __integrity_failed_exiting_action(self) -> None:
        self._robot.led_blinkers.turn_off(side=SideBlinkers.Side.BOTH)

    def __integrity_succeeded_entering_action(self) -> None:
        print("Everything is well. Proceeding as planned.")
        self._robot.change_couleur((0, 255, 0), SideBlinkers.Side.BOTH)
        self._robot.eye_blinkers.blink2(SideBlinkers.Side.BOTH, 3.0, 1.0, 0.5, True, False)

    def __shutdown_robot_entering_action(self) -> None:
        print("Shutting down.")
        self._robot.change_couleur((0, 255, 255), SideBlinkers.Side.RIGHT_RECIPROCAL)
        self._robot.eye_blinkers.blink2(side=SideBlinkers.Side.RIGHT_RECIPROCAL, cycle_duration=1.0,
                                        total_duration=3.0, end_off=False)
        self._robot.shut_down()

    def track(self) -> bool:
        self._robot.eye_blinkers.track()
        self._robot.led_blinkers.track()
        self.__task1.track()
        return super().track()


class ManualControl(RobotState):

    def track(self):
        self.fsm.track()

    class StopState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(robot, parameters)  # TODO:validation
            self.custom_value = 'stop'

        def _do_entering_action(self) -> None:
            print(self._robot.led_blinkers.is_on(SideBlinkers.Side.BOTH))
            if self.entry_count > 1:
                self._robot.led_blinkers.turn_off(SideBlinkers.Side.BOTH)
            self._robot.stop()

    class RotateRightState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(robot, parameters)  # TODO:validation
            self.custom_value = 'Right'

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.blink1(SideBlinkers.Side.RIGHT, 1.0, 0.50, True)
            self._robot.right()

    class RotateLeftState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(robot, parameters)  # TODO:validation
            self.custom_value = 'Left'

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.blink1(SideBlinkers.Side.LEFT, 1.0, 0.50, True)
            self._robot.left()

    class ForwardState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(robot, parameters)  # TODO:validation
            self.custom_value = 'Forward'

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.blink1(SideBlinkers.Side.BOTH, 1.0, 0.25, True)
            self._robot.foward()

    class BackwardState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(robot, parameters)  # TODO:validation
            self.custom_value = 'Backward'

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.blink1(SideBlinkers.Side.BOTH, 1.0, 0.75)
            self._robot.backward()

    def __init__(self, remoteControl, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
        super().__init__(robot, parameters)  # TODO:validation
        self.__rotate_left = self.RotateLeftState(self._robot)
        self.__forward = self.ForwardState(self._robot)
        self.__stop = self.StopState(self._robot)
        self.__rotate_right = self.RotateRightState(self._robot)
        self.__backwards = self.BackwardState(self._robot)
        self._remote_control = remoteControl

        FiniteStateMachine._purple_link('left', self.__stop, self.__rotate_left, self._remote_control)

        FiniteStateMachine._purple_link('', self.__rotate_left, self.__stop, self._remote_control)

        FiniteStateMachine._purple_link('down', self.__stop, self.__backwards, self._remote_control)

        FiniteStateMachine._purple_link('', self.__backwards, self.__stop, self._remote_control)

        FiniteStateMachine._purple_link('right', self.__stop, self.__rotate_right, self._remote_control)

        FiniteStateMachine._purple_link('', self.__rotate_right, self.__stop, self._remote_control)

        FiniteStateMachine._purple_link('up', self.__stop, self.__forward, self._remote_control)

        FiniteStateMachine._purple_link('', self.__forward, self.__stop, self._remote_control)

        self.__layout = FiniteStateMachine.Layout()
        self.__layout.initial_state = self.__stop
        self.__layout.add_state(self.__stop)
        self.__layout.add_state(self.__forward)
        self.__layout.add_state(self.__backwards)
        self.__layout.add_state(self.__rotate_left)
        self.__layout.add_state(self.__rotate_right)
        self.fsm = FiniteStateMachine(self.__layout)

    def _do_entering_action(self) -> None:
        self.fsm.track()


c64 = C64Project()
c64.run()




