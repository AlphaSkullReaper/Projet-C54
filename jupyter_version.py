
import easygopigo3 as easy
my_gopigo = easy.EasyGoPiGo3()

import time
from abc import abstractmethod, ABC
from datetime import datetime
from enum import Enum
from time import perf_counter
from re import A
from tkinter.messagebox import NO
from typing import Callable, Optional, List
from copy import deepcopy



class Transition(ABC):
    def __init__(self, next_state: 'State' = None):
        if isinstance(next_state, State):
            self.__next_state = next_state
        else:
            raise Exception("ERROR STATE NOT VALID")

    @property
    def is_valid(self) -> bool:
        return self.__next_state is not None

    @property
    def next_state(self) -> 'State':
        return self.__next_state

    @next_state.setter
    def next_state(self, new_state: 'State'):
        if isinstance(new_state, State):
            self.__next_state = new_state
        else:
            error = f"ERROR: Transition's new_state is of the wrong type. Expected STATE, received {type(new_state)}"
            raise Exception(error)

    @abstractmethod
    def is_transiting(self) -> bool:
        pass

    def _do_transiting_action(self) -> None:
        pass

    def _exec_transiting_action(self) -> None:
        self._do_transiting_action()


class State:
    class Parameters:
        def __init__(self, terminal: bool = False, do_in_state_when_entering: bool = False,
                     do_in_state_action_when_exiting: bool = False):
            self.terminal: bool = terminal
            self.do_in_state_when_entering: bool = do_in_state_when_entering
            self.do_in_state_action_when_exiting: bool = do_in_state_action_when_exiting

    def __init__(self, parameters: 'Parameters' = Parameters()) -> None:
        self.__parameters = parameters
        self.__transition: list['Transition'] = []

    @property
    def get_transitionList(self):
        return self.__transition

    @property
    def is_valid(self) -> 'bool':
        if len(self.__transition) >= 1:
            for val in self.__transition:
                if not val.is_valid:
                    return False
        return True

    @property
    def is_terminal(self) -> bool:
        return self.__parameters.terminal

    @property
    def is_transiting(self) -> 'Transition' or None:
        if len(self.__transition) >= 1:
            for val in self.__transition:
                if val.is_transiting():
                    return val
        else:
            return None

    def add_transition(self, next_transition: 'Transition') -> None:
        if isinstance(next_transition, Transition):
            self.__transition.append(next_transition)
        else:
            raise Exception("Error: Expecting a Type Transition!")

    def _do_entering_action(self) -> None:
        pass

    def _do_in_state_action(self) -> None:
        pass

    def _do_exiting_action(self) -> None:
        pass

    def _exec_entering_action(self) -> None:
        self._do_entering_action()
        if self.__parameters.do_in_state_when_entering:
            self._exec_in_state_action()

    def _exec_in_state_action(self) -> None:
        self._do_in_state_action()

    def _exec_exiting_action(self) -> None:
        if self.__parameters.do_in_state_action_when_exiting:
            self._exec_in_state_action()
        self._do_exiting_action()


StateList = list
ConditionList = list


class FiniteStateMachine:
    class OperationalState(Enum):
        UNINITIALIZED = 1
        IDLE = 2
        RUNNING = 3
        TERMINAL_REACHED = 4

    class Layout:
        def __init__(self) -> None:
            self.states = []
            self._initial_state = None

        @property
        def is_valid(self) -> bool:
            validity = False
            if self.states.__contains__(self.initial_state):
                for a_state in self.states:
                    if a_state.is_valid:
                        validity = True
                    else:
                        validity = False

            return validity

        @property
        def initial_state(self) -> 'State':
            return self._initial_state

        @initial_state.setter
        def initial_state(self, new_state: 'State') -> None:
            if new_state.is_valid:
                self._initial_state = new_state

        def add_state(self, new_state: 'State') -> None:
            if new_state.is_valid:
                self.states.append(new_state)

        def add_states(self, list_states: StateList) -> None:
            for a_state in list_states:
                if a_state.is_valid:
                    self.states.append(a_state)

                    # les setters, on veut trap les erreurs le plus vite possible: is instance, raise exeption is false

    def __init__(self, layout_parameter: 'Layout', uninitialized: bool = True) -> None:  # do typing layount:Layount
        if layout_parameter.is_valid:
            self.__layout = layout_parameter
        else:
            raise Exception("Layount non valide")
        self.__current_applicative_state = None
        self.__current_operational_state = self.OperationalState.UNINITIALIZED if uninitialized \
            else self.OperationalState.IDLE

    @property
    def current_applicative_state(self) -> 'State':
        return self.__current_applicative_state

    @property
    def current_operational_state(self) -> 'OperationalState':
        return self.__current_operational_state

    # Track, si le current state est terminal fais rien.
    # 3 conditions pour arrêter le while L is etat terminal, quand operational state n'es tpas running, et la troisième si le
    def run(self, reset: bool = True, time_budget: float = None) -> None:
        self.test_timer = time.perf_counter()
        start_time = perf_counter()
        current_track_state = True
        # reset on stop, reset bool before track,
        if reset:
            self.reset()
        if self.__current_operational_state is not self.OperationalState.TERMINAL_REACHED \
                or self.__current_operational_state is not self.OperationalState.UNINITIALIZED:
            while current_track_state and (time_budget is None or perf_counter() - start_time < time_budget):
                current_track_state = self.track()
            self.stop()

        # Un pas de simulation de la résolution du state machine.
        # self.__current_operational_state = self.OperationalState.RUNNING

    def track(self) -> bool:
        if self.__current_operational_state == self.OperationalState.UNINITIALIZED:
            self.__current_applicative_state = self.__layout.initial_state
            self.__current_operational_state = self.OperationalState.IDLE
            self.__current_applicative_state._exec_entering_action()

        if self.__current_operational_state == self.OperationalState.TERMINAL_REACHED:
            self.__current_applicative_state._exec_exiting_action()
            return False

        else:
            self.__current_operational_state = self.OperationalState.RUNNING
            transition = self.__current_applicative_state.is_transiting
            if transition is not None:
                self._transit_by(transition)
                self.__current_applicative_state._exec_in_state_action()
            else:
                self.__current_applicative_state._exec_in_state_action()
            return True

    def stop(self) -> None:
        self.__current_operational_state = self.OperationalState.IDLE

    def reset(self) -> None:
        self.__current_operational_state = self.OperationalState.IDLE
        self.__current_applicative_state = self.__layout.initial_state  # ON PUISSE REPARTE LA BOUCLE WHILE DE RUN

    def transit_to(self, state: 'State') -> None:
        if self.__current_applicative_state is not None:
            self.__current_applicative_state._exec_exiting_action()
        self.__current_applicative_state = state
        self.__current_operational_state = FiniteStateMachine.OperationalState.IDLE
        self.__current_applicative_state._exec_entering_action()

    def _transit_by(self, transition: 'Transition') -> None:
        if transition.next_state.is_terminal:
            self.__current_operational_state = self.OperationalState.TERMINAL_REACHED
        self.__current_applicative_state._exec_exiting_action()
        transition._exec_transiting_action()
        self.__current_applicative_state = transition.next_state
        self.__current_applicative_state._exec_entering_action()


"""
           ______________________________________
  ________|                                      |_______
  \       |         CONDITIONALTRANSITION        |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""


class ConditionalTransition(Transition):
    def __init__(self, condition: 'Condition' = None, next_state: 'State' = None):
        super().__init__(next_state)
        if isinstance(condition, Condition):
            self.__condition = condition

    @property
    def is_valid(self) -> bool:
        if self.__condition is not None:
            if self.next_state is not None:
                return True
        else:
            return False

    @property
    def condition(self) -> 'Condition':
        return self.__condition

    @condition.setter
    def condition(self, new_condition) -> None:
        self.__condition = new_condition

    # chaque objet a une valeur bool, en overridant __bool__, on détermine quand condition est valide
    # https://docs.python.org/3/reference/datamodel.html?highlight=__bool__#object.__bool__
    def is_transiting(self) -> bool:
        return bool(self.__condition)


class Condition:
    def __init__(self, inverse: bool = False):
        self.__inverse = inverse

    @abstractmethod
    def _compare(self) -> bool:
        pass

    # https://docs.python.org/3/reference/datamodel.html?highlight=__bool__#object.__bool__
    def __bool__(self) -> bool:
        return self._compare() ^ self.__inverse


"""
           ______________________________________
  ________|                                      |_______
  \       |         ALWAYSTRUECONDITION          |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""


class AlwaysTrueCondition(Condition):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def _compare(self) -> bool:
        return True


"""
           ______________________________________
  ________|                                      |_______
  \       |            VALUECONDITION            |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""


class ValueCondition(Condition):
    def __init__(self, initial_value: any, expected_value: any, inverse: bool = False):
        super().__init__(inverse)
        self.expected_value: any = expected_value
        self.value: any = initial_value

    def _compare(self) -> bool:
        return True if self.value == self.expected_value else False


"""
           ______________________________________
  ________|                                      |_______
  \       |           TIMEDCONDITION             |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\  
"""


class TimedCondition(Condition):
    def __init__(self, duration: float = 1., time_reference: float = None, inverse: bool = False):
        super().__init__(inverse)
        self.__counter_duration: float = duration
        if time_reference is None:
            self.__counter_reference = time.perf_counter()
        else:
            self.__counter_reference = time_reference

    def _compare(self) -> bool:
        return time.perf_counter() - self.__counter_reference >= self.__counter_duration

    @property
    def duration(self) -> float:
        return self.__counter_duration

    @duration.setter
    def duration(self, new_duration: float) -> None:
        self.__counter_duration = new_duration
        if isinstance(new_duration, float):
            self.__counter_duration = new_duration
        else:
            error = f"ERROR: TimedCondition's new_duration is of the wrong type. Expected FLOAT, received " \
                    f"{type(new_duration)} "
            raise Exception(error)

    def reset(self):
        self.__counter_reference = time.perf_counter()


"""
           ______________________________________
  ________|                                      |_______
  \       |           MANYCONDITIONS             |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 

"""

"""     
----------------8<-------------[ ManyConditions ]--------------- 
"""


class ManyConditions(Condition):

    def __init__(self, inverse: bool = False):
        super().__init__(inverse)
        self._conditions: list[Condition] = []

    def add_condition(self, condition: 'Condition'):
        self._conditions.append(condition)

    def add_conditions(self, condition_list: ConditionList):
        self._conditions.extend(condition_list)


"""     
----------------8<-------------[ AllConditions ]----------------- 
"""


class AllConditions(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def _compare(self) -> bool:
        return all(self._conditions)


"""     
----------------8<-------------[ AnyConditions ]----------------- 
"""


class AnyConditions(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def _compare(self) -> bool:
        return any(self._conditions)


"""     
----------------8<-------------[ NoneConditions ]---------------- 
"""


class NoneConditions(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def _compare(self) -> bool:
        return not all(self._conditions)


"""
           ______________________________________
  ________|                                      |_______
  \       |        MONITOREDSTATECONDITION       |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 

"""


class MonitoredStateCondition(Condition):
    def __init__(self, monitered_state: 'MonitoredState', inverse: bool = False):
        if isinstance(monitered_state, MonitoredState):
            super().__init__(inverse)
            self._monitered_state = monitered_state

    @property
    def monitered_state(self) -> 'MonitoredState':
        return self._monitered_state

    @monitered_state.setter
    def monitered_state(self, monitered_state: 'MonitoredState'):
        if isinstance(monitered_state, MonitoredState):
            self._monitered_state = monitered_state
        else:
            error = f"ERROR: MonitoredStateCondition's monitered_state is of the wrong type. Expected MonitoredState, " \
                    f"received {type(monitered_state)} "
            raise Exception(error)


"""     
----------------8<-------------[ StateEntryDurationCondition ]------ 
"""


class StateEntryDurationCondition(MonitoredStateCondition):
    def __init__(self, duration: float, monitered_state: 'MonitoredState', inverse: bool = False):
        super().__init__(monitered_state, inverse)
        self.__duration = duration

    def _compare(self) -> bool:
        return time.perf_counter() - self._monitered_state.last_entry_time >= self.__duration

    @property
    def duration(self) -> float:
        return self.__duration

    @duration.setter
    def duration(self, new_duration):
        if isinstance(new_duration, float):
            self.__duration = new_duration
        else:
            error = f"ERROR: StateEntryDurationCondition's new_duration is of the wrong type. Expected FLOAT, " \
                    f"received {type(new_duration)}"
            raise Exception(error)


"""     
----------------8<-------------[ StateEntryCountCondition ]--------- 
"""


class StateEntryCountCondition(MonitoredStateCondition):
    def __init__(self, expected_count: int, monitered_state: 'MonitoredState', auto_reset: bool = False,
                 inverse: bool = False):
        super().__init__(monitered_state, inverse)
        self.__auto_reset = auto_reset
        self.__expected_count = expected_count
        self.__ref_count = self._monitered_state.entry_count

    def _compare(self) -> bool:

        if self.__ref_count == self.__expected_count:
            self.reset_count()
            return True
        else:
            return False

    def reset_count(self):
        self.__ref_count = self._monitered_state.entry_count

    @property
    def expected_count(self) -> int:
        return self.__expected_count

    @expected_count.setter
    def expected_count(self, new_expected_count):
        self.__expected_count = new_expected_count

        if isinstance(new_expected_count, int):
            self.__expected_count = new_expected_count
        else:
            error = f"ERROR: StateEntryCountCondition's new_expected_count is of the wrong type. Expected INT, received {type(new_expected_count)}"
            raise Exception(error)


"""     
----------------8<-------------[ StateValueCondition ]------------- 
"""


class StateValueCondition(MonitoredStateCondition):
    def __init__(self, expected_value: any, monitered_state: 'MonitoredState', inverse: bool = False):
        super().__init__(monitered_state, inverse)
        self.__expected_value = expected_value

    def _compare(self) -> bool:
        return self._monitered_state.custom_value == self.expected_value

    @property
    def expected_value(self) -> any:
        return self.__expected_value

    @expected_value.setter
    def expected_value(self, new_expected_value: any):
        self.__expected_value = new_expected_value


"""
           ______________________________________
  ________|                                      |_______
  \       |           ACTIONTRANSITION           |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""


class ActionTransition(ConditionalTransition):
    Action = Callable[[], None]

    def __init__(self, condition: Condition = None, next_state: State = None):
        super().__init__(condition, next_state)
        self.__transiting_actions: list[ActionTransition.Action] = []

    def _do_transiting_action(self):
        for action in self.__transiting_actions:
            action()

    def add_transiting_action(self, action: Action):
        if isinstance(action, Callable):
            self.__transiting_actions.append(action)
        else:
            raise Exception("ERROR: Invalid Transiting Action")


"""
           ______________________________________
  ________|                                      |_______
  \       |          MONITOREDTRANSITION         |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""


class MonitoredTransition(ActionTransition):
    def __init__(self, condition: Condition = None, next_state: 'State' = None):
        super().__init__(condition, next_state)
        self.__transit_count: int = 0
        self.__last_transit_time: float = 0
        self.custom_value: any = None

    @property
    def transit_count(self) -> int:
        return self.__transit_count

    @property
    def last_transit_time(self) -> float:
        return self.__last_transit_time

    def reset_transit_count(self):
        self.__transit_count = 0

    def reset_last_transit_time(self):
        self.__last_transit_time = time.perf_counter()

    def _exec_transiting_action(self):
        self.__last_transit_time = time.perf_counter()
        self.__transit_count += 1

        super()._exec_transiting_action()


class ActionState(State):
    Action = Callable[[], None]

    def __init__(self, parameters: 'State.Parameters' = State.Parameters()) -> None:
        super().__init__(parameters)
        self.__entering_action: list[ActionState.Action] = []
        self.__in_state_action: list[ActionState.Action] = []
        self.__exiting_actions: list[ActionState.Action] = []

    def _do_entering_action(self) -> None:
        for action in self.__entering_action:
            action()

    def _do_in_state_action(self) -> None:
        for action in self.__in_state_action:
            action()

    def _do_exiting_action(self) -> None:
        for action in self.__exiting_actions:
            action()

    def add_entering_action(self, action: Callable) -> None:
        if isinstance(action, Callable):
            self.__entering_action.append(action)
        else:
            raise Exception("Error: Expecting Type Action")

    def add_in_state_action(self, action: 'Callable') -> None:
        if isinstance(action, Callable):
            self.__in_state_action.append(action)
        else:
            raise Exception("Error: Expecting Type Action")

    def add_exiting_action(self, action: 'Callable') -> None:
        if isinstance(action, Callable):
            self.__exiting_actions.append(action)
        else:
            raise Exception("Error: Expecting Type Action")


class MonitoredState(ActionState):

    def __init__(self, parameters: 'State.Parameters' = State.Parameters()) -> None:
        super().__init__(parameters)
        self.__counter_last_entry: float = 0
        self.__counter_last_exit: float = 0
        self.__entry_count: int = 0
        self.custom_value: any = None

    @property
    def entry_count(self) -> int:
        return self.__entry_count

    @property
    def last_entry_time(self) -> float:
        return self.__counter_last_entry

    @property
    def last_exit_time(self) -> float:
        return self.__counter_last_exit

    def reset_entry_count(self) -> None:
        self.__entry_count = 0

    def reset_last_times(self) -> None:
        val = time.perf_counter()
        self.__counter_last_entry = val
        self.__counter_last_exit = val

    def _exec_entering_action(self) -> None:
        self.__counter_last_entry = time.perf_counter()
        self.__entry_count += 1
        super()._exec_entering_action()

    def _exec_exiting_action(self) -> None:
        self.__counter_last_exit = time.perf_counter()
        super()._exec_exiting_action()


# Functor
StateGenerator = Callable[[], MonitoredState]


class Blinker(FiniteStateMachine):
    def __init__(self, off_state_generator: 'StateGenerator',
                 on_state_generator: 'StateGenerator') -> None:
        layout = FiniteStateMachine.Layout()
        state_list = []
        self.__off = off_state_generator()
        self.__on = on_state_generator()
        self.__off_duration = off_state_generator()
        self.__on_duration = on_state_generator()
        self.__blink_on = off_state_generator()
        self.__blink_off = on_state_generator()
        self.__blink_stop_off = off_state_generator()
        self.__blink_stop_on = on_state_generator()
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
        self.__left_blinker = Blinker( left_off_state_generator, left_on_state_generator)
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
    def __init__(self, robot:'Robot'):
        self.__robot = robot
        super().__init__(lambda: LedBlinkers.LedOffLeftState(self.__robot), lambda: LedBlinkers.LedOnLeftState(self.__robot),
                         lambda: LedBlinkers.LedOffRightState(self.__robot), lambda: LedBlinkers.LedOnRightState(self.__robot))

    class LedOnLeftState(MonitoredState):
        def __init__(self, robot, parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(parameters)
            self.custom_value = True
            self.__robot = robot
            self.__position = 1

        @property
        def position(self) -> int:
            return self.__position

        def _do_entering_action(self) -> None:
            self.__robot.led_on(self.__position)

    class LedOffLeftState(MonitoredState):
        def __init__(self, robot, parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(parameters)
            self.custom_value = False
            self.__robot = robot
            self.__position = 1

        @property
        def position(self) -> int:
            return self.__position

        def _do_entering_action(self) -> None:
            self.__robot.led_off(self.__position)

    class LedOnRightState(MonitoredState):
        def __init__(self, robot, parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(parameters)
            self.custom_value = True
            self.__robot = robot
            self.__position = 0

        @property
        def position(self) -> int:
            return self.__position

        def _do_entering_action(self) -> None:
            self.__robot.led_on(self.__position)

    class LedOffRightState(MonitoredState):
        def __init__(self, robot, parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(parameters)
            self.custom_value = False
            self.__robot = robot
            self.__position = 0

        @property
        def position(self) -> int:
            return self.__position

        def _do_entering_action(self) -> None:
            self.__robot.led_off(self.__position)


class EyeBlinkers(SideBlinkers):
    def __init__(self, robot:'Robot'):
        self.__robot = robot
        super().__init__(lambda: EyeBlinkers.EyeOffLeftState(self.__robot), lambda: EyeBlinkers.EyeOnLeftState(self.__robot),
                         lambda: EyeBlinkers.EyeOffRightState(self.__robot), lambda: EyeBlinkers.EyeOnRightState(self.__robot))

    class EyeOnLeftState(MonitoredState):
        def __init__(self, robot, parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(parameters)
            self.custom_value = True
            self.__robot = robot
            self.__couleur =(255,0,0)
            self.__position = 1

        @property
        def position(self) -> int:
            return self.__position

        @property
        def couleur(self) -> tuple:
            return self.__couleur

        @couleur.setter
        def couleur(self,value:tuple):
            self.__couleur = value
            self.__robot.set_left_eye_color(self.__couleur)

        def _do_entering_action(self) -> None:
            self.__robot.open_left_eye()

    class EyeOffLeftState(MonitoredState):
        def __init__(self, robot, parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(parameters)
            self.custom_value = False
            self.__robot = robot
            self.__couleur = (255,0,0)
            self.__position = 1

        @property
        def position(self) -> int:
            return self.__position

        @property
        def couleur(self) -> tuple:
            return self.__couleur

        @couleur.setter
        def couleur(self, value: tuple):
            self.__couleur = value
            self.__robot.set_left_eye_color(self.__couleur)

        def _do_entering_action(self) -> None:
            self.__robot.close_left_eye()

    class EyeOnRightState(MonitoredState):
        def __init__(self, robot, parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(parameters)
            self.custom_value = True
            self.__robot = robot
            self.__couleur =(255,0,0)
            self.__position = 1

        @property
        def position(self) -> int:
            return self.__position

        @property
        def couleur(self) -> tuple:
            return self.__couleur

        @couleur.setter
        def couleur(self, value: tuple):
            self.__couleur = value
            self.__robot.set_right_eye_color(self.__couleur)

        def _do_entering_action(self) -> None:
            self.__robot.open_right_eye()

    class EyeOffRightState(MonitoredState):
        def __init__(self, robot, parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(parameters)
            self.custom_value = False
            self.__robot = robot
            self.__couleur = None
            self.__position = 1

        @property
        def position(self) -> int:
            return self.__position

        @property
        def couleur(self) -> tuple:
            return self.__couleur

        @couleur.setter
        def couleur(self, value: tuple):
            self.__couleur = value
            self.__robot.set_right_eye_color(self.__couleur)

        def _do_entering_action(self) -> None:
            self.__robot.close_right_eye()







blinker = Blinker(MonitoredState, MonitoredState)

ledBLinko = LedBlinkers(my_gopigo)

ledBLinko.blink4(SideBlinkers.Side.LEFT, 3, 5.0, 0.5, False, True)

while(True):
    ledBLinko.track()
# pass

# blink_1 = type('blink_1', (), {"test": float})
#
# o = blink_1()
# type(o) # my_type
# print(isinstance(o, blink_1)) # True
# print(isinstance(o, int)) # False

#sideBlinker = SideBlinkers(MonitoredState, MonitoredState, MonitoredState, MonitoredState)
#sideBlinker.is_on(SideBlinkers.Side.RIGHT)
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

