from niveau1 import FiniteStateMachine, State
from niveau2 import MonitoredState, ActionState, ConditionalTransition, MonitoredTransition, \
    StateEntryDurationCondition, StateEntryCountCondition, StateValueCondition
from enum import Enum
from typing import Callable
from copy import deepcopy

# Functor
StateGenerator = Callable[[], MonitoredState]


def factory_method_monitored_state(value: any = None):
    ms = MonitoredState()
    if value is not None:
        ms.custom_value = value
    return ms


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
        self.__blink_stop_on = on_state_generator()
        self.__blink_stop_on.custom_value = True

        self.__blink_begin = MonitoredState()

        self.__blink_stop_begin = MonitoredState()
        self.__blink_stop_end = MonitoredState()

        self.__off_duration_to_on = self.__green_link(self.__off_duration,
                                                      self.__on)

        self.__on_duration_to_off = self.__green_link(original_state=self.__on_duration,
                                                      destination_state=self.__off)

        self.__blink_on_to_blink_off = self.__green_link(original_state=self.__blink_on,
                                                         destination_state=self.__blink_off)
        self.__blink_off_to_blink_on = self.__green_link(original_state=self.__blink_off,
                                                         destination_state=self.__blink_on)

        self.__blink_stop_off_to_blink_stop_on = self.__green_link(original_state=self.__blink_stop_off,
                                                                   destination_state=self.__blink_stop_on)

        self.__blink_stop_on_to_blink_stop_off = self.__green_link(original_state=self.__blink_stop_on,
                                                                   destination_state=self.__blink_stop_off)

        self.__blink_begin_to_blink_off = self.__orange_link(original_state=self.__blink_begin,
                                                             destination_state=self.__blink_off,
                                                             expected_value=False
                                                             )
        self.__blink_begin_to_blink_on = self.__orange_link(original_state=self.__blink_begin,
                                                            destination_state=self.__blink_on,
                                                            expected_value=True)

        self.__blink_stop_off_to_blink_stop_end_by_blink_stop_begin = self.__doted_green_link(
            original_state=self.__blink_stop_off,
            destination_state=self.__blink_stop_end,
            intermediary_monitored_state=self.__blink_stop_begin
        )
        self.__blink_stop_on_to_blink_stop_end_by_blink_stop_begin = self.__doted_green_link(
            original_state=self.__blink_stop_on,
            intermediary_monitored_state=self.__blink_stop_begin,
            destination_state=self.__blink_stop_end
        )

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
        state_entry_duration_condition = StateEntryDurationCondition(duration=0,
                                                                     monitered_state=original_state)
        conditional_transition = ConditionalTransition(condition=state_entry_duration_condition,
                                                       next_state=destination_state)
        original_state.add_transition(next_transition=conditional_transition)

        return conditional_transition.condition

    @staticmethod
    def __doted_green_link(original_state: MonitoredState,
                           destination_state: MonitoredState,
                           intermediary_monitored_state: MonitoredState):
        state_entry_duration_condition = StateEntryDurationCondition(duration=0,
                                                                     monitered_state=intermediary_monitored_state)
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
        self.__blink_stop_on_to_blink_stop_end_by_blink_stop_begin.duration = total_duration
        self.__blink_stop_off_to_blink_stop_end_by_blink_stop_begin.duration = total_duration
        self.__blink_stop_off_to_blink_stop_on = cycle_duration * percent_on
        self.__blink_stop_on_to_blink_stop_off = cycle_duration - cycle_duration * percent_on
        self.__blink_stop_on.custom_value = begin_on
        self.__blink_stop_off.custom_value = end_off
        self.transit_to(self.__blink_stop_begin)

    def blink3(self,
               total_duration: float,
               n_cycle: int,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        self.__blink_stop_on_to_blink_stop_end_by_blink_stop_begin.duration = total_duration * percent_on
        self.__blink_stop_off_to_blink_stop_end_by_blink_stop_begin.duration \
            = total_duration - total_duration * percent_on
        self.__blink_stop_on.custom_value = begin_on
        self.__blink_stop_off.custom_value = end_off
        for cycle in range(n_cycle):
            self.transit_to(self.__blink_stop_begin)

    def blink4(self,
               n_cycle: int,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):

        self.__blink_stop_off_to_blink_stop_on = cycle_duration * percent_on
        self.__blink_stop_on_to_blink_stop_off = cycle_duration - cycle_duration * percent_on
        self.__blink_stop_on.custom_value = begin_on
        self.__blink_stop_off.custom_value = end_off
        for cycle in range(n_cycle):
            self.transit_to(self.__blink_stop_begin)


class SideBlinkers:
    class Side(Enum):
        LEFT = 1
        RIGHT = 2
        BOTH = 3
        LEFT_RECIPROCAL = 4
        RIGHT_RECIPROCAL = 5

    def __init__(self, left_blinker: Blinker,
                 right_blinker: Blinker):
        self.left_blinker = left_blinker
        self.right_blinker = right_blinker

    def SideBlinker(self,
                    left_off_state_generator: StateGenerator,
                    left_on_state_generator: StateGenerator,
                    right_off_state_generator: StateGenerator,
                    right_on_state_generator: StateGenerator):
        pass

    def is_on(self, side: Side) -> bool:
        pass

    def is_off(self, side: Side) -> bool:
        pass

    def turn_off(self, side: Side) -> None:
        pass

    def turn_on(self, side: Side) -> None:
        pass

    def turn_off2(self, side: Side, duration: float) -> None:
        pass

    def turn_on2(self, side: Side, duration: float) -> None:
        pass

    def blink1(self, side: Side,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True):
        pass

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
        pass


blinker = Blinker(MonitoredState, MonitoredState)
blinker.blink2(total_duration=20.0, cycle_duration=2.0, percent_on=0.5)
blinker.run(False)

# blink_1 = type('blink_1', (), {"test": float})
#
# o = blink_1()
# type(o) # my_type
# print(isinstance(o, blink_1)) # True
# print(isinstance(o, int)) # False
