from typing import Callable
import time
from niveau1 import Transition, State, ConditionList
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
        else:
            raise Exception("L'intrant condition n'est pas de type Condition")

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
        if not isinstance(new_condition, Condition):
            raise Exception("L'intrant new_condition n'est pas de type Condition")
        self.__condition = new_condition

    # chaque objet a une valeur bool, en overridant __bool__, on détermine quand condition est valide
    # https://docs.python.org/3/reference/datamodel.html?highlight=__bool__#object.__bool__
    def is_transiting(self) -> bool:
        return bool(self.__condition)


"""
           ______________________________________
  ________|                                      |_______
  \       |           RemoteTransition           |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""


class RemoteControlTransition(ConditionalTransition):
    def __init__(self, condition: 'Condition' = None, next_state: 'RobotState' = None,
                 remote_control: 'RemoteControl' = None):
        if remote_control.__class__.__name__ != "Remote":
            raise Exception("L'intrant remotecontrol n'est pas 'Remote' mais plutôt", remotecontrol.__class__.__name__)

        # if not isinstance(remote_control, easysensors.Remote):
        #    raise Exception("L'intrant remotecontrol n'est pas de type easysensors.Remote")
        self._remote_control = remote_control

        super().__init__(condition, next_state)
        # todo: bouncing


"""
           ______________________________________
  ________|                                      |_______
  \       |              CONDITION               |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""


class Condition:
    def __init__(self, inverse: bool = False):
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")
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
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")
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
        if initial_value is None:
            raise Exception("L'intrant initial value n'est pas donner ou est Null")
        if expected_value is None:
            raise Exception("L'intrant expected value  n'est pas donner ou est Null")
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")
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
    def __init__(self, duration: float = 1.0, time_reference: float = None, inverse: bool = False):
        if not isinstance(duration, float):
            raise Exception("L'intrant duration n'est pas de type float")
        if not isinstance(time_reference, float):
            raise Exception("L'intrant time_reference n'est pas de type float")
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")

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
            raise Exception("L'intrant new_duration n'est pas de type float")

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


class ManyConditions(Condition):

    def __init__(self, inverse: bool = False):
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")
        super().__init__(inverse)
        self._conditions: list[Condition] = []

    def add_condition(self, condition: 'Condition'):
        if not isinstance(condition, Condition):
            raise Exception("L'intrant condition n'est pas de type Condition")
        self._conditions.append(condition)

    def add_conditions(self, condition_list: ConditionList):
        if not isinstance(condition_list, list):
            raise Exception("L'intrant condition_list n'est pas de type list")
        for condition in condition_list:
            if not isinstance(condition, Condition):
                raise Exception("L'intrant condition_list a au moins un élément qui n'est pas de type Condition")
        self._conditions.extend(condition_list)


"""
           ______________________________________
  ________|                                      |_______
  \       |            ALLCONDITIONS             |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 

"""


class AllConditions(ManyConditions):
    def __init__(self, inverse: bool = False):
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")
        super().__init__(inverse)

    def _compare(self) -> bool:
        return all(self._conditions)


"""
           ______________________________________
  ________|                                      |_______
  \       |            ANYCONDITIONS             |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 

"""


class AnyConditions(ManyConditions):
    def __init__(self, inverse: bool = False):
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")
        super().__init__(inverse)

    def _compare(self) -> bool:
        return any(self._conditions)


"""
           ______________________________________
  ________|                                      |_______
  \       |           NONECONDITIONS             |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 

"""


class NoneConditions(ManyConditions):
    def __init__(self, inverse: bool = False):
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")
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
        else:
            raise Exception("L'intrant monitered_state n'est pas de type MonitoredState")
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")

    @property
    def monitered_state(self) -> 'MonitoredState':
        return self._monitered_state

    @monitered_state.setter
    def monitered_state(self, next_monitered_state: 'MonitoredState'):
        if isinstance(next_monitered_state, MonitoredState):
            self._monitered_state = next_monitered_state
        else:
            raise Exception("L'intrant next_monitered_state n'est pas de type MonitoredState")


"""
           ______________________________________
  ________|                                      |_______
  \       |      STATEENTRYDURATIONCONDITION     |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 

"""


class StateEntryDurationCondition(MonitoredStateCondition):
    def __init__(self, duration: float, monitered_state: 'MonitoredState', inverse: bool = False):
        if not isinstance(monitered_state, MonitoredState):
            raise Exception("L'intrant monitered_state n'est pas de type MonitoredState")
        if not isinstance(duration, float):
            raise Exception("L'intrant duration n'est pas de type float")
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")

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
            raise Exception("L'intrant new_duration n'est pas de type bool")


"""
           ______________________________________
  ________|                                      |_______
  \       |       StateEntryCountCondition       |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 

"""


class StateEntryCountCondition(MonitoredStateCondition):
    def __init__(self, expected_count: int, monitered_state: 'MonitoredState', auto_reset: bool = False,
                 inverse: bool = False):
        if not isinstance(monitered_state, MonitoredState):
            raise Exception("L'intrant monitered_state n'est pas de type MonitoredState")
        if not isinstance(expected_count, int):
            raise Exception("L'intrant expected_count n'est pas de type int")
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")
        if not isinstance(auto_reset, bool):
            raise Exception("L'intrant auto_reset n'est pas de type bool")

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
            raise Exception("L'intrant new_expected_count n'est pas de type int")


"""
           ______________________________________
  ________|                                      |_______
  \       |          StateValueCondition         |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 

"""


class StateValueCondition(MonitoredStateCondition):
    def __init__(self, expected_value: any, monitered_state: 'MonitoredState', inverse: bool = False):
        if not isinstance(monitered_state, MonitoredState):
            raise Exception("L'intrant monitered_state n'est pas de type MonitoredState")
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")
        if expected_value is None:
            raise Exception("L'intrant expected_value n'est pas présent ou null")

        super().__init__(monitered_state, inverse)

        self.__expected_value = expected_value

    def _compare(self) -> bool:
        return self._monitered_state.custom_value == self.expected_value

    @property
    def expected_value(self) -> any:
        return self.__expected_value

    @expected_value.setter
    def expected_value(self, new_expected_value: any):
        if new_expected_value is None:
            raise Exception("L'intrant expected_value n'est pas présent ou null")

        self.__expected_value = new_expected_value


"""
           ______________________________________
  ________|                                      |_______
  \       |         RemoteValueCondition         |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 

"""


class RemoteValueCondition(Condition):
    def __init__(self, expected_value: str, remote_control: 'RemoteControl' = None, inverse: bool = False):
        self._remote_control = remote_control
        self.__keycodes = ['', 'up', 'left', 'ok', 'right', 'down', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*',
                           '0', '#']
        if expected_value in self.__keycodes:
            self.__expected_value = expected_value
        else:
            raise Exception("Expected value must be a valid keycode ")
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")
        if remote_control.__class__.__name__ != "Remote":
            raise Exception("L'intrant remotecontrol n'est pas 'Remote' mais plutôt", remotecontrol.__class__.__name__)

        # if not isinstance(remote_control, easysensors.Remote):
        #    raise Exception("L'intrant remotecontrol n'est pas de type easysensors.Remote")

        super().__init__(inverse)

    def _compare(self) -> bool:

        return self._remote_control.get_remote_code() == self.__expected_value

    @property
    def expected_value(self) -> str:
        return self.__expected_value

    @expected_value.setter
    def expected_value(self, new_expected_value: str):
        if new_expected_value in self.__keycodes:
            self.__expected_value = new_expected_value
        else:
            raise Exception("Expected value must be a valid keycode")


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


class RobotState(MonitoredState):
    def __init__(self, a_robot, parameters: 'State.Parameters' = State.Parameters()) -> None:
        self._robot = a_robot
        super().__init__(parameters)