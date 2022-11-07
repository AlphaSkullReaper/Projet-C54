from re import A
from tkinter.messagebox import NO
from typing import Callable
import time
from niveau1 import Transition, State
from abc import abstractmethod

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
            print(self.next_state)
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

    def add_conditions(self, condition_list: list[Condition]):
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
    def __init__(self, expected_count: int, monitered_state: 'State', auto_reset: bool = False, inverse: bool = False):
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
    def __init__(self, expected_value: any, monitered_state: 'State', inverse: bool = False):
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

    def __init__(self, next_state: State = None):
        super().__init__(next_state)
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
    def __init__(self, next_state: 'State' = None):
        super().__init__(next_state)
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

    def exec_entering_action(self) -> None:
        self.__counter_last_entry = time.perf_counter()
        self.__entry_count += 1
        super()._do_entering_action()
        if self.__parameters.do_in_state_when_entering:
            self._exec_in_state_action()

    def exec_exiting_action(self) -> None:
        if self.__parameters.do_in_state_action_when_exiting:
            self._exec_in_state_action()
        super()._do_exiting_action()
        self.__counter_last_exit = time.perf_counter()
