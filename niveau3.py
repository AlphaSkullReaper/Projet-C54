from niveau1 import FiniteStateMachine, State
from niveau2 import MonitoredState, ActionState, ConditionalTransition, MonitoredTransition, \
    StateEntryDurationCondition, StateEntryCountCondition, StateValueCondition
from enum import Enum
from typing import Callable
from copy import deepcopy
from manual_control import GoPiGo3

# Functor
StateGenerator = Callable[[], MonitoredState]


class Blinker(FiniteStateMachine):
    def __init__(self, off_state_generator: 'StateGenerator',
                 on_state_generator: 'StateGenerator') -> None:
        layout = FiniteStateMachine.Layout()
        state_list = []
        self.__off = off_state_generator()
        self.__off.custom_value = False
        self.__on = on_state_generator()
        self.__on.custom_value = True
        self.__off_duration = off_state_generator()
        self.__off_duration.custom_value = False
        self.__on_duration = on_state_generator()
        self.__on.custom_value = True

        self.__blink_on = off_state_generator()
        self.__blink_on.custom_value = True
        self.__blink_off = on_state_generator()
        self.__blink_off.custom_value = False

        self.__blink_stop_off = off_state_generator()
        self.__blink_stop_off.custom_value = False
        self.__blink_stop_off.add_entering_action(lambda: print("YELLING STOP OFF"))
        self.__blink_stop_on = on_state_generator()
        self.__blink_stop_on.custom_value = True
        self.__blink_stop_on.add_entering_action(lambda: print("YELLING STOP ON"))

        self.__blink_begin = MonitoredState()

        self.__blink_stop_begin = MonitoredState()
        self.__blink_stop_begin.add_entering_action(lambda: print("YELLING STOP BEGIN"))
        self.__blink_stop_end = MonitoredState()
        self.__blink_stop_end.add_entering_action(lambda: print("YELLING STOP END"))

        self.__off_duration_to_on = self.__green_link(self.__off_duration,
                                                      self.__on)

        self.__on_duration_to_off = self.__green_link(original_state=self.__on_duration,
                                                      destination_state=self.__off)

        self.__blink_on_to_blink_off = self.__green_link(original_state=self.__blink_on,
                                                         destination_state=self.__blink_off)
        self.__blink_off_to_blink_on = self.__green_link(original_state=self.__blink_off,
                                                         destination_state=self.__blink_on)

        self.__blink_begin_to_blink_off = self.__orange_link(original_state=self.__blink_begin,
                                                             destination_state=self.__blink_off,
                                                             expected_value=False
                                                             )
        self.__blink_begin_to_blink_on = self.__orange_link(original_state=self.__blink_begin,
                                                            destination_state=self.__blink_on,
                                                            expected_value=True)

        self.__blink_stop_off_to_blink_stop_end = self.__doted_green_link(original_state=self.__blink_stop_off,
                                                                          destination_state=self.__blink_stop_end,
                                                                          ownerState=self.__blink_stop_begin)
        self.__blink_stop_on_to_blink_stop_end = self.__doted_green_link(original_state=self.__blink_stop_on,
                                                                         destination_state=self.__blink_stop_end,
                                                                         ownerState=self.__blink_stop_begin)

        self.__blink_stop_off_to_blink_stop_on = self.__green_link(original_state=self.__blink_stop_off,
                                                                   destination_state=self.__blink_stop_on)

        self.__blink_stop_on_to_blink_stop_off = self.__green_link(original_state=self.__blink_stop_on,
                                                                   destination_state=self.__blink_stop_off)

        self.__blink_stop_begin_to_blink_stop_off = self.__orange_link(original_state=self.__blink_stop_begin,
                                                                       destination_state=self.__blink_stop_off,
                                                                       expected_value=False
                                                                       )
        self.__blink_stop_begin_to_blink_stop_on = self.__orange_link(original_state=self.__blink_stop_begin,
                                                                      destination_state=self.__blink_stop_on,
                                                                      expected_value=True)

        self.__blink_stop_end_to_off = self.__orange_link(original_state=self.__blink_stop_end,
                                                          destination_state=self.__off,
                                                          expected_value=False
                                                          )
        self.__blink_stop_end_to_on = self.__orange_link(original_state=self.__blink_stop_end,
                                                         destination_state=self.__on,
                                                         expected_value=True)

        state_list.append(self.__on)
        state_list.append(self.__off_duration)
        state_list.append(self.__on_duration)
        state_list.append(self.__blink_on)
        state_list.append(self.__blink_off)
        state_list.append(self.__blink_stop_off)
        state_list.append(self.__blink_stop_on)
        state_list.append(self.__blink_begin)
        state_list.append(self.__blink_stop_begin)
        state_list.append(self.__blink_stop_end)

        layout.initial_state = self.__off
        layout.add_state(self.__off)
        layout.add_states(state_list)
        super().__init__(layout)

    @staticmethod
    def __green_link(original_state: MonitoredState,
                     destination_state: MonitoredState):
        state_entry_duration_condition = StateEntryDurationCondition(duration=1.0,
                                                                     monitered_state=original_state)
        conditional_transition = ConditionalTransition(condition=state_entry_duration_condition,
                                                       next_state=destination_state)
        original_state.add_transition(next_transition=conditional_transition)

        return conditional_transition.condition

    @staticmethod
    def __doted_green_link(original_state: MonitoredState,
                           destination_state: MonitoredState,
                           ownerState: MonitoredState):
        state_entry_duration_condition = StateEntryDurationCondition(duration=1.0,
                                                                     monitered_state=ownerState)
        conditional_transition = ConditionalTransition(condition=state_entry_duration_condition,
                                                       next_state=destination_state)
        original_state.add_transition(next_transition=conditional_transition)

        return conditional_transition.condition

    @staticmethod
    def __orange_link(original_state: MonitoredState, destination_state: MonitoredState, expected_value: bool):
        state_value_condition = StateValueCondition(expected_value=expected_value,
                                                    monitered_state=original_state)
        conditional_transition = ConditionalTransition(condition=state_value_condition,
                                                       next_state=destination_state)
        original_state.add_transition(conditional_transition)
        return conditional_transition.condition

    @property
    def is_on(self) -> bool:
        return self.current_applicative_state == self.__on

    @property
    def is_off(self) -> bool:
        return self.current_applicative_state == self.__off

    def turn_on1(self) -> None:
        self.transit_to(self.__on)

    def turn_off1(self) -> None:
        self.transit_to(self.__off)

    def turn_on2(self, duration: float) -> None:
        self.__off_duration_to_on.duration = duration
        self.transit_to(self.__off_duration)

    def turn_off2(self, duration: float) -> None:
        self.__on_duration_to_off.duration = duration
        self.transit_to(self.__on_duration)

    def blink1(self,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True):
        self.__blink_begin.custom_value = begin_on
        self.__blink_off_to_blink_on.duration = cycle_duration * percent_on
        self.__blink_on_to_blink_off.duration = cycle_duration - cycle_duration * percent_on
        self.transit_to(self.__blink_begin)

    def blink2(self,
               total_duration: float,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        self.__blink_stop_begin.custom_value = begin_on
        self.__blink_stop_end.custom_value = end_off

        self.__blink_stop_off_to_blink_stop_on.duration = cycle_duration * percent_on
        self.__blink_stop_on_to_blink_stop_off.duration = cycle_duration - (cycle_duration * percent_on)

        self.__blink_stop_off_to_blink_stop_end.duration = total_duration
        self.__blink_stop_on_to_blink_stop_end.duration = total_duration

        self.transit_to(self.__blink_stop_begin)

    def blink3(self,
               total_duration: float,
               n_cycle: int,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        self.__blink_stop_begin.custom_value = begin_on
        self.__blink_stop_end.custom_value = end_off

        self.__blink_stop_on_to_blink_stop_end.duration = total_duration
        self.__blink_stop_off_to_blink_stop_end.duration = total_duration

        self.__blink_stop_off_to_blink_stop_on.duration = (total_duration / n_cycle) * percent_on
        self.__blink_stop_on_to_blink_stop_off.duration = (total_duration / n_cycle) - (
                (total_duration / n_cycle) * percent_on)

        self.transit_to(self.__blink_stop_begin)

    def blink4(self,
               n_cycle: int,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        self.__blink_stop_begin.custom_value = begin_on
        self.__blink_stop_end.custom_value = end_off

        self.__blink_stop_on_to_blink_stop_end.duration = n_cycle * cycle_duration
        self.__blink_stop_off_to_blink_stop_end.duration = n_cycle * cycle_duration

        self.__blink_stop_off_to_blink_stop_on = cycle_duration * percent_on
        self.__blink_stop_on_to_blink_stop_off = cycle_duration - (cycle_duration * percent_on)

        self.transit_to(self.__blink_stop_begin)


class SideBlinkers:
    class Side(Enum):
        LEFT = 1
        RIGHT = 2
        BOTH = 3
        LEFT_RECIPROCAL = 4
        RIGHT_RECIPROCAL = 5

    def __init__(self,
                 left_off_state_generator: StateGenerator,
                 left_on_state_generator: StateGenerator,
                 right_off_state_generator: StateGenerator,
                 right_on_state_generator: StateGenerator):
        self.__left_blinker = Blinker(left_on_state_generator, left_off_state_generator)
        self.__right_blinker = Blinker(right_off_state_generator, right_on_state_generator)

    def is_on(self, side: Side) -> bool:
        if side == SideBlinkers.Side.LEFT:
            return self.__left_blinker.is_on
        elif side == SideBlinkers.Side.RIGHT:
            return self.__right_blinker.is_on
        elif side == SideBlinkers.Side.BOTH:
            return self.__right_blinker.is_on and self.__left_blinker.is_on
        elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
            return self.__left_blinker.is_on and self.__right_blinker.is_off
        elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
            return self.__right_blinker.is_on and self.__left_blinker.is_off

    def is_off(self, side: Side) -> bool:
        if side == SideBlinkers.Side.LEFT:
            return self.__left_blinker.is_off
        elif side == SideBlinkers.Side.RIGHT:
            return self.__right_blinker.is_off
        elif side == SideBlinkers.Side.BOTH:
            return self.__right_blinker.is_off and self.__left_blinker.is_off
        elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
            return self.__left_blinker.is_off and self.__right_blinker.is_on
        elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
            return self.__right_blinker.is_off and self.__left_blinker.is_on

    def turn_off(self, side: Side) -> None:
        if side == SideBlinkers.Side.LEFT:
            self.__left_blinker.turn_off1()
        elif side == SideBlinkers.Side.RIGHT:
            self.__right_blinker.turn_off1()
        elif side == SideBlinkers.Side.BOTH:
            self.__right_blinker.turn_off1()
            self.__left_blinker.turn_off1()
        elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
            self.__left_blinker.turn_off1()
            self.__right_blinker.turn_on1()
        elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
            self.__right_blinker.turn_off1()
            self.__left_blinker.turn_on1()

    def turn_on(self, side: Side) -> None:
        if side == SideBlinkers.Side.LEFT:
            self.__left_blinker.turn_on1()
        elif side == SideBlinkers.Side.RIGHT:
            self.__right_blinker.turn_on1()
        elif side == SideBlinkers.Side.BOTH:
            self.__right_blinker.turn_on1()
            self.__left_blinker.turn_on1()
        elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
            self.__left_blinker.turn_on1()
            self.__right_blinker.turn_off1()
        elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
            self.__right_blinker.turn_on1()
            self.__left_blinker.turn_off1()

    # TODO TEST!
    def turn_off2(self, side: Side, duration: float) -> None:
        if side == SideBlinkers.Side.LEFT:
            self.__left_blinker.turn_off2(duration)
        elif side == SideBlinkers.Side.RIGHT:
            self.__right_blinker.turn_off2(duration)
        elif side == SideBlinkers.Side.BOTH:
            self.__right_blinker.turn_off2(duration)
            self.__left_blinker.turn_off2(duration)
        elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
            self.__left_blinker.turn_off2(duration)
            self.__right_blinker.turn_on2(duration)
        elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
            self.__right_blinker.turn_off2(duration)
            self.__left_blinker.turn_on2(duration)

    # TODO TEST!
    def turn_on2(self, side: Side, duration: float) -> None:
        if side == SideBlinkers.Side.LEFT:
            self.__left_blinker.turn_on2(duration)
        elif side == SideBlinkers.Side.RIGHT:
            self.__right_blinker.turn_on2(duration)
        elif side == SideBlinkers.Side.BOTH:
            self.__right_blinker.turn_on2(duration)
            self.__left_blinker.turn_on2(duration)
        elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
            self.__left_blinker.turn_on2(duration)
            self.__right_blinker.turn_off2(duration)
        elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
            self.__right_blinker.turn_on2(duration)
            self.__left_blinker.turn_off2(duration)

    # TODO verif if percent_on is a percentage
    def blink1(self, side: Side,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True):
        if side == SideBlinkers.Side.LEFT:
            self.__left_blinker.blink1(cycle_duration, percent_on, begin_on)
        elif side == SideBlinkers.Side.RIGHT:
            self.__right_blinker.blink1(cycle_duration, percent_on, begin_on)
        elif side == SideBlinkers.Side.BOTH:
            self.__left_blinker.blink1(cycle_duration, percent_on, begin_on)
            self.__right_blinker.blink1(cycle_duration, percent_on, begin_on)
        elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
            self.__left_blinker.blink1(cycle_duration, percent_on, begin_on)
            self.__right_blinker.blink1(cycle_duration, percent_on, not begin_on)
        elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
            self.__left_blinker.blink1(cycle_duration, percent_on, not begin_on)
            self.__right_blinker.blink1(cycle_duration, percent_on, begin_on)

    def blink2(self, side: Side,
               total_duration: float,
               cycle_duration: float = 1,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if side == SideBlinkers.Side.LEFT:
            self.__left_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinkers.Side.RIGHT:
            self.__right_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinkers.Side.BOTH:
            self.__left_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on, end_off)
            self.__right_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
            self.__left_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on, not end_off)
            self.__right_blinker.blink2(total_duration, cycle_duration, percent_on, not begin_on, end_off)
        elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
            self.__left_blinker.blink2(total_duration, cycle_duration, percent_on, not begin_on, end_off)
            self.__right_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on, not end_off)

    def blink3(self, side: Side,
               total_duration: float,
               n_cycle: int,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if side == SideBlinkers.Side.LEFT:
            self.__left_blinker.blink3(total_duration, n_cycle, percent_on, begin_on, end_off)
        elif side == SideBlinkers.Side.RIGHT:
            self.__right_blinker.blink3(total_duration, n_cycle, percent_on, begin_on, end_off)
        elif side == SideBlinkers.Side.BOTH:
            self.__left_blinker.blink3(total_duration, n_cycle, percent_on, begin_on, end_off)
            self.__right_blinker.blink3(total_duration, n_cycle, percent_on, begin_on, end_off)
        elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
            self.__left_blinker.blink3(total_duration, n_cycle, percent_on, begin_on, not end_off)
            self.__right_blinker.blink3(total_duration, n_cycle, percent_on, not begin_on, end_off)
        elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
            self.__left_blinker.blink3(total_duration, n_cycle, percent_on, not begin_on, end_off)
            self.__right_blinker.blink3(total_duration, n_cycle, percent_on, begin_on, not end_off)

    def blink4(self,
               side: Side,
               n_cycle: int,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if side == SideBlinkers.Side.LEFT:
            self.__left_blinker.blink4(n_cycle, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinkers.Side.RIGHT:
            self.__right_blinker.blink4(n_cycle, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinkers.Side.BOTH:
            self.__left_blinker.blink4(n_cycle, cycle_duration, percent_on, begin_on, end_off)
            self.__right_blinker.blink4(n_cycle, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
            self.__left_blinker.blink4(n_cycle, cycle_duration, percent_on, begin_on, not end_off)
            self.__right_blinker.blink4(n_cycle, cycle_duration, percent_on, not begin_on, end_off)
        elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
            self.__left_blinker.blink4(n_cycle, cycle_duration, percent_on, not begin_on, end_off)
            self.__right_blinker.blink4(n_cycle, cycle_duration, percent_on, begin_on, not end_off)

    def track(self) -> None:
        self.__left_blinker.track()
        self.__right_blinker.track()


class LedBlinkers(SideBlinkers):
    class Position(Enum):
        LEFT = 0
        RIGHT = 1

    # TODO: fix position problem

    class LedState(MonitoredState):
        def __init__(self, ledState: bool, color: tuple, position: 'Position',
                     parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(parameters)
            self.custom_value = ledState
            self.color = color
            self.position = position


class EyeBlinkers:
    def __init__(self):
        pass


class Robot:
    def __init__(self):
        self.__robot = GoPiGo3()
        self.__led_blinkers = LedBlinkers()
        self.__eyes_blinkers = EyeBlinkers()

    @property
    def robot(self) -> 'GoPiGo3':
        return self.__robot

    @property
    def led_blinkers(self) -> 'LedBlinkers':
        return self.__led_blinkers

    @property
    def eye_blinkers(self) -> 'EyeBlinkers':
        return self.__eyes_blinkers

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

    def drive_cm(self, dist: float, blocking: bool = True) -> None:
        self.__robot.drive_cm(dist, blocking)

    def drive_inches(self, dist: float, blocking: bool = True) -> None:
        self.__robot.drive_inches(dist, blocking)

    def drive_degrees(self, degrees: float, blocking: bool = True):  # TODO: Check return without follow up
        return self.__robot.drive_degrees(degrees, blocking)

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
        self.__robot.steer(left_percent, right_percent)

    def orbit(self, degrees: int, radius_cm: int = 0, blocking: bool = True):  # TODO: Check return without follow up
        return self.__robot.orbit(degrees, radius_cm, blocking)

    def target_reached(self, left_target_degrees: int, right_target_degrees: int) -> bool:
        return self.__robot.target_reached(left_target_degrees, right_target_degrees)

    def reset_encoders(self, blocking: bool = True) -> None:
        return self.__robot.reset_encoders(blocking)

    def read_encoders_average(self, units: str = "cm") -> float:
        return self.robot.read_encoders_average(units)

    def turn_degrees(self, degrees: int, blocking: bool = True) -> None:
        self.turn_degrees(degrees, blocking)

    def blinker_on(self, id: int) -> None:
        self.__robot.blinker_on(id)

    def blinker_off(self, id: int) -> None:
        self.__robot.blinker_off(id)

    def lef_on(self, id: int) -> None:
        self.__robot.led_on(id)

    def lef_off(self, id: int) -> None:
        self.__robot.led_off(id)

    def set_left_eye_color(self, color: tuple) -> None:
        self.__robot.set_left_eye_color(color)

    def set_right_eye_color(self, color: tuple) -> None:
        self.__robot.set_right_eye_color(color)

    def set_eye_color(self, color: tuple) -> None:
        self.__robot.set_eye_color(color)

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
        return self.__robot.init_light_sensor(port)

    def init_sound_sensor(self, port: str = "AD1"):  # TODO easysensors.SoundSensor
        return self.__robot.init_sound_sensor(port)

    def init_loudness_sensor(self, port: str = "AD1"):
        return self.__robot.init_loudness_sensor(port)

    def init_ultrasonic_sensor(self, port: str = "AD1"):
        return self.__robot.init_ultrasonic_sensor(port)

    def init_buzzer(self, port: str = "AD1"):
        return self.__robot.init_buzzer(port)

    def init_led(self, port: str = "AD1"):
        return self.__robot.init_led(port)

    def init_button_sensor(self, port: str = "AD1"):
        return self.__robot.init_button_sensor(port)

    def init_line_follower(self, port: str = "I2C"):
        return self.__robot.init_line_follower(port)

    def init_servo(self, port: str = "SERVO1"):
        return self.__robot.init_servo(port)

    def init_distance_sensor(self, port: str = "I2C"):
        return self.__robot.init_distance_sensor(port)

    def init_light_color_sensor(self, port: str = "I2C", led_state=True):
        return self.__robot.init_light_color_sensor(port)

    def init_imu_sensor(self, port: str = "I2C"):
        return self.__robot.init_imu_sensor(port)

    def init_dht_sensor(self, sensor_type: int = 0):
        return self.__robot.init_dht_sensor(sensor_type)

    def init_remote(self, port: str = "AD1"):
        return self.__robot.init_remote(port)

    def init_motion_sensor(self, port: str = "AD1"):
        return self.__robot.init_motion_sensor(port)


class C64Project(FiniteStateMachine):
    def __init__(self):
        self.robot = Robot()

        layout = FiniteStateMachine.Layout()

        # layout.initial_state = self.__off
        # layout.add_state(self.__off)
        #
        super().__init__(layout)

    def start(self) -> None:
        print("It's Starting Time!")
        pass

    # TODO: call the stategenerator but with the led state. Create 4 different state generator with 4 different state preiniatialed
    # TODO: track function calls the track function of the sideBlinker (add more to it?)
    # implements the gopigo librarie here or in the robot class. Could create all 4 base state in each blinker, create all 4 state generator,
    # have the track function call the side eye blinker track.


blinker = Blinker(MonitoredState, MonitoredState)

# blinker.blink4(5, 2.0)
# blinker.blink4(2, 5.0)
# blinker.blink1()
# blinker.run(False)
# pass

# blink_1 = type('blink_1', (), {"test": float})
#
# o = blink_1()
# type(o) # my_type
# print(isinstance(o, blink_1)) # True
# print(isinstance(o, int)) # False

sideBlinker = SideBlinkers(MonitoredState, MonitoredState, MonitoredState, MonitoredState)
sideBlinker.is_on(SideBlinkers.Side.RIGHT)
# sideBlinker.track()
# sideBlinker.turn_off(SideBlinkers.Side.BOTH)
# print("LEFT OFF?", sideBlinker.is_off(SideBlinkers.Side.LEFT))
# print("RIGHT OFF?", sideBlinker.is_off(SideBlinkers.Side.RIGHT))

# sideBlinker.turn_on2(SideBlinkers.Side.LEFT, 300000.0)
# print("LEFT OFF?", sideBlinker.is_off(SideBlinkers.Side.LEFT))
# print("RIGHT OFF?", sideBlinker.is_off(SideBlinkers.Side.RIGHT))
# sideBlinker.turn_on(SideBlinkers.Side.BOTH)
# print("LEFT OFF?", sideBlinker.is_off(SideBlinkers.Side.LEFT))
# print("RIGHT OFF?", sideBlinker.is_off(SideBlinkers.Side.RIGHT))

sideBlinker.blink4(SideBlinkers.Side.LEFT, 3)
sideBlinker.track()
