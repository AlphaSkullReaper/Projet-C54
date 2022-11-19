from niveau1 import FiniteStateMachine, State
from niveau2 import MonitoredState, ActionState, ConditionalTransition, MonitoredTransition, \
    StateEntryDurationCondition, StateEntryCountCondition, StateValueCondition
from enum import Enum
from typing import Callable

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
        pipioppi = State.Parameters(False, False, False)

        self.off = off_state_generator(pipioppi)
        self.on = on_state_generator(pipioppi)

        #BLINK BEGIN
        #State
        self.blink_begin = MonitoredState()
        self.blink_begin_on_state = on_state_generator()
        self.blink_begin_off_state = off_state_generator()
        #condition
        self.state_entry_duration_condition_blink_begin_onstate_to_Offstate = StateEntryDurationCondition( 0,self.blink_begin_on_state,True)
        self.state_entry_duration_condition_blink_begin_offstate_to_Onstate = StateEntryDurationCondition(0,self.blink_begin_off_state,True)
        self.state_value_condition_blink_being_to_off_state = StateValueCondition( False,self.blink_begin,True)
        self.state_value_condition_for_blink_being_to_on_state  = StateValueCondition( True,self.blink_begin,True)
        #Transition
        self.transition_blink_begin_on_state_to_off_state = ConditionalTransition(self.state_entry_duration_condition_blink_begin_onstate_to_Offstate , self.blink_begin_off_state)
        self.transition_blink_begin_off_state_to_on_state = ConditionalTransition(
           self.state_entry_duration_condition_blink_begin_offstate_to_Onstate,  self.blink_begin_on_state)
        self.transition_blink_begin_to_off_state = ConditionalTransition( self.state_value_condition_blink_being_to_off_state, self.blink_begin_off_state)
        self.transition_blink_begin_to_on_state = ConditionalTransition( self.state_value_condition_for_blink_being_to_on_state,   self.blink_begin_on_state)

        self.blink_begin_on_state.add_transition(self.transition_blink_begin_on_state_to_off_state)
        self.blink_begin_off_state.add_transition(self.transition_blink_begin_off_state_to_on_state)
        self.blink_begin.add_transition(self.transition_blink_begin_to_off_state)
        self.blink_begin.add_transition(self.transition_blink_begin_to_on_state)

        layout.add_states([self.blink_begin,self.blink_begin_on_state,self.blink_begin_off_state])

        # self.state_entry_duration_condition_off = StateEntryDurationCondition(1.0, self.off)
        # self.conditional_condition_off = ConditionalTransition(
        #     self.state_entry_duration_condition_off,
        #     self.on)
        # self.state_entry_duration_condition_on = StateEntryDurationCondition(1.0, self.on)
        # self.conditional_condition_on = ConditionalTransition(self.state_entry_duration_condition_on,
        #                                                       self.off)

        # self.off_duration.add_transition(...)
        #
        # layout.add_state(self.off)
        # layout.add_state(self.on)

        layout.initial_state = self.off
        layout.add_state(self.on)
        layout.add_state(layout.initial_state)

        # self.off_duration = off_state_generator()
        # self.on_duration = on_state_generator()
        # self.state_entry_duration_condition_off_duration = StateEntryDurationCondition(1.0, self.off_duration)
        # self.conditional_condition_off_duration = ConditionalTransition(
        #     self.state_entry_duration_condition_off_duration,
        #     self.on_duration)
        # self.state_entry_duration_condition_on_duration = StateEntryDurationCondition(1.0, self.on_duration)
        # self.conditional_condition_on_duration = ConditionalTransition(self.state_entry_duration_condition_on_duration,
        #                                                                self.off_duration)
        #
        # self.blink_off = off_state_generator()
        # self.blink_on = on_state_generator()
        # self.state_entry_duration_condition_blink_off = StateEntryDurationCondition(1.0, self.blink_off)
        # self.conditional_condition_blink_off = ConditionalTransition(
        #     self.state_entry_duration_condition_blink_off,
        #     self.blink_on)
        # self.state_entry_duration_condition_blink_on = StateEntryDurationCondition(1.0, self.blink_on)
        # self.conditional_condition_blink_on = ConditionalTransition(self.state_entry_duration_condition_blink_on,
        #                                                             self.blink_off)
        #
        # self.blink_stop_off = off_state_generator()
        # self.blink_stop_on = on_state_generator()
        # self.state_entry_duration_condition_blink_stop_off = StateEntryDurationCondition(1.0, self.blink_stop_off)
        # self.conditional_condition_blink_stop_off = ConditionalTransition(
        #     self.state_entry_duration_condition_blink_stop_off,
        #     self.blink_on)
        # self.state_entry_duration_condition_blink_stop_on = StateEntryDurationCondition(1.0, self.blink_stop_on)
        # self.conditional_condition_blink_stop_on = ConditionalTransition(
        #     self.state_entry_duration_condition_blink_stop_on,
        #     self.blink_stop_off)

        # self.state_value_condition_off = StateValueCondition(0, self.off)
        # self.state_value_condition_on = StateValueCondition(0, self.on)

        # #Temporary Params
        # param_1 = State.Parameters()
        # param_2 = State.Parameters()
        # param_3 = State.Parameters()
        #
        # self.blink_begin = MonitoredState(param_1)
        # self.blink_stop_begin = MonitoredState(param_2)
        # self.blink_stop_end = MonitoredState(param_3)
        #
        # self.state_value_condition_blink_begin = StateValueCondition(0, self.blink_begin)
        # self.state_value_condition_blink_stop_begin = StateValueCondition(0, self.blink_stop_begin)
        # self.state_value_condition_blink_stop_end = StateValueCondition(0, self.blink_stop_end)

        super().__init__(layout)

    @property
    def is_on(self) -> bool:
        return self.current_applicative_state == self.on

    @property
    def is_off(self) -> bool:
        return self.current_applicative_state == self.off

    def turn_on(self, duration: float) -> None:
        pass

    def turn_off(self, duration: float) -> None:
        pass

    def turn_on(self) -> None:
        self.transit_to(self.on)

    def turn_off(self) -> None:
        self.transit_to(self.off)

    def blink1(self,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True):
        self.blink_begin.custom_value = begin_on
        self.state_entry_duration_condition_blink_begin_offstate_to_Onstate.duration = cycle_duration
        self.state_entry_duration_condition_blink_begin_offstate_to_off = cycle_duration


    def blink2(self,
               total_duration: float,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        pass

    def blink3(self, total_duration: float,
               n_cycle: int,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        pass

    def blink4(self,
               n_cycle: int,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        pass


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
blinker.run()




# blink_1 = type('blink_1', (), {"test": float})
#
# o = blink_1()
# type(o) # my_type
# print(isinstance(o, blink_1)) # True
# print(isinstance(o, int)) # False
