from niveau1 import FiniteStateMachine, State
from niveau2 import MonitoredState, ActionState, ConditionalTransition, MonitoredTransition, \
    StateEntryDurationCondition, StateEntryCountCondition, StateValueCondition
from enum import Enum
from typing import Callable
from copy import deepcopy

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
        self.__blink_stop_end.custom_value = begin_on

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
        pass

    def blink3(self, side: Side,
               total_duration: float,
               n_cycle: int,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        pass

    def blink4(self,
               side: Side,
               n_cycle: int,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        pass

    def track(self) -> None:
        self.__left_blinker.track()
        self.__right_blinker.track()


class LedBlinkers(SideBlinkers):
    class Position(Enum):
        LEFT = 0
        RIGHT = 1

 #TODO: fix position problem

    class LedState(MonitoredState):
        def __init__(self, ledState: bool, color: tuple, position: 'Position',
                     parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(parameters)
            self.custom_value = ledState
            self.color = color
            self.position = position

    #TODO: call the stategenerator but with the led state. Create 4 different state generator with 4 different state preiniatialed
    #TODO: track function calls the track function of the sideBlinker (add more to it?)
    #implements the gopigo librarie here or in the robot class. Could create all 4 base state in each blinker, create all 4 state generator,
    #have the track function call the side eye blinker track.

blinker = Blinker(MonitoredState, MonitoredState)
blinker.blink4(5, 2.0)
# blinker.blink4(2, 5.0)
# blinker.blink1()
blinker.run(False)
pass

# blink_1 = type('blink_1', (), {"test": float})
#
# o = blink_1()
# type(o) # my_type
# print(isinstance(o, blink_1)) # True
# print(isinstance(o, int)) # False

# sideBlinker = SideBlinkers(MonitoredState,MonitoredState,MonitoredState,MonitoredState)
# sideBlinker.is_on(SideBlinkers.Side.RIGHT)
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
