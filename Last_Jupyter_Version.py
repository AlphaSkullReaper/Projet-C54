import doctest
import time
from abc import abstractmethod, ABC
from enum import Enum
from time import perf_counter
from typing import Callable


##     ## #### ##     ## #########    ###    ##     ##            ##
###    ##  ##  ##     ## ##          ## ##   ##     ##          ####
####   ##  ##  ##     ## ##         ##   ##  ##     ##            ##
## ##  ##  ##  ##     ## #######   ##     ## ##     ##            ##
##   ####  ##   ##   ##  ##        ######### ##     ##            ##
##    ###  ##    ## ##   ##        ##     ## ##     ##            ##
##     ## ####    ###    ######### ##     ##  #######           ######

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
            raise Exception("Next_Transition: Expecting Transition Input")

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


class Transition(ABC):
    def __init__(self, next_state: 'State' = None):
        if isinstance(next_state, State):
            self.__next_state = next_state
        else:
            raise Exception("Next_State: Expecting State Input")

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
            raise Exception("New_State: Expecting State Input")

    @abstractmethod
    def is_transiting(self) -> bool:
        pass

    def _do_transiting_action(self) -> None:
        pass

    def _exec_transiting_action(self) -> None:
        self._do_transiting_action()

    @staticmethod
    def __main_doctest():
        import test
        doctest.testmod()  # verbose=True)


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
            if not isinstance(new_state, State):
                raise Exception("New_State: Expecting State Input")
            if new_state.is_valid:
                self._initial_state = new_state

        def add_state(self, new_state: 'State') -> None:
            if not isinstance(new_state, State):
                raise Exception("New_State: Expecting State Input")
            if new_state.is_valid:
                self.states.append(new_state)

        def add_states(self, list_states: StateList) -> None:
            if not isinstance(list_states, list):
                raise Exception("List_State: Expecting List Input")
            for state in list_states:
                if not isinstance(state, State):
                    raise Exception("Error: At Least One Element of List_State Is Not A State")

            for a_state in list_states:
                if a_state.is_valid:
                    self.states.append(a_state)

                    # les setters, on veut trap les erreurs le plus vite possible: is instance, raise exeption is false

    def __init__(self, layout_parameter: 'Layout', uninitialized: bool = True) -> None:  # do typing layout:Layout
        if not isinstance(layout_parameter, FiniteStateMachine.Layout):
            raise Exception("Layout_Parameter: Expecting Layout Input")
        if not isinstance(uninitialized, bool):
            raise Exception("Uninitialized: Expecting Bool Type")

        if layout_parameter.is_valid:
            self.__layout = layout_parameter
        else:
            raise Exception("Layout_Parameter: Layout Input Is Invalid")
        self.__current_applicative_state = None
        self.__current_operational_state = self.OperationalState.UNINITIALIZED if uninitialized \
            else self.OperationalState.IDLE

    @property
    def current_applicative_state(self) -> 'State':
        return self.__current_applicative_state

    @property
    def current_operational_state(self) -> 'OperationalState':
        return self.__current_operational_state

    def run(self, reset: bool = True, time_budget: float = None) -> None:
        if not isinstance(reset, bool):
            raise Exception("Reset: Expecting Bool Input")

        if time_budget is not None:
            if not isinstance(time_budget, float):
                raise Exception("Time_Budget: Expecting Float Input")
        self.test_timer = time.perf_counter()
        start_time = perf_counter()
        current_track_state = True

        if reset:
            self.reset()
        if self.__current_operational_state is not self.OperationalState.TERMINAL_REACHED \
                or self.__current_operational_state is not self.OperationalState.UNINITIALIZED:
            while current_track_state and (time_budget is None or perf_counter() - start_time < time_budget):
                current_track_state = self.track()
            self.stop()

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
        self.__current_applicative_state = self.__layout.initial_state
        self.__current_applicative_state._exec_entering_action()  # ON PUISSE REPARTE LA BOUCLE WHILE DE RUN

    def transit_to(self, state: 'State') -> None:
        if not isinstance(state, State):
            raise Exception("State: Expecting State Type")
        if self.__current_applicative_state is not None:
            self.__current_applicative_state._exec_exiting_action()
        self.__current_applicative_state = state
        self.__current_operational_state = FiniteStateMachine.OperationalState.IDLE
        self.__current_applicative_state._exec_entering_action()

    def _transit_by(self, transition: 'Transition') -> None:

        if not isinstance(transition, Transition):
            raise Exception("Transition: Expecting Transition Input")
        if transition.next_state.is_terminal:
            self.__current_operational_state = self.OperationalState.TERMINAL_REACHED
        self.__current_applicative_state._exec_exiting_action()
        transition._exec_transiting_action()
        self.__current_applicative_state = transition.next_state
        self.__current_applicative_state._exec_entering_action()

    @staticmethod
    def _green_link(original_state: 'MonitoredState',
                    destination_state: 'MonitoredState',
                    duration: float = 1.0):
        if not isinstance(original_state, MonitoredState):
            raise Exception("Original_State: Expecting MonitoredState Input (Or Child Of)")

        if not isinstance(destination_state, MonitoredState):
            raise Exception("Destination_State: Expecting MonitoredState Input (Or Child Of)")
        state_entry_duration_condition = StateEntryDurationCondition(duration=duration,
                                                                     monitered_state=original_state)
        conditional_transition = ConditionalTransition(condition=state_entry_duration_condition,
                                                       next_state=destination_state)
        original_state.add_transition(next_transition=conditional_transition)

        return conditional_transition.condition

    @staticmethod
    def _doted_green_link(original_state: 'MonitoredState',
                          destination_state: 'MonitoredState',
                          ownerState: 'MonitoredState'):

        if not isinstance(original_state, MonitoredState):
            raise Exception("Original_State: Expecting MonitoredState Input (Or Child Of)")

        if not isinstance(destination_state, MonitoredState):
            raise Exception("Destination_State: Expecting MonitoredState Input (Or Child Of)")

        if not isinstance(ownerState, MonitoredState):
            raise Exception("OwnerState: Expecting MonitoredState Input (Or Child Of)")

        state_entry_duration_condition = StateEntryDurationCondition(duration=1.0,
                                                                     monitered_state=ownerState)
        conditional_transition = ConditionalTransition(condition=state_entry_duration_condition,
                                                       next_state=destination_state)
        original_state.add_transition(next_transition=conditional_transition)

        return conditional_transition.condition

    @staticmethod
    def _orange_link(original_state: 'MonitoredState', destination_state: 'MonitoredState', expected_value: bool):
        if not isinstance(original_state, MonitoredState):
            raise Exception("Original_State: Expecting MonitoredState Input (Or Child Of)")

        if not isinstance(destination_state, MonitoredState):
            raise Exception("Destination_State: Expecting MonitoredState Input (Or Child Of)")

        if not isinstance(expected_value, bool):
            raise Exception("Expected_Value: Expecting Bool Input")

        state_value_condition = StateValueCondition(expected_value=expected_value,
                                                    monitered_state=original_state)
        conditional_transition = ConditionalTransition(condition=state_value_condition,
                                                       next_state=destination_state)
        original_state.add_transition(conditional_transition)
        return conditional_transition.condition

    @staticmethod
    def _blue_link(original_state: 'MonitoredState', destination_state: 'MonitoredState'):
        if not isinstance(original_state, MonitoredState):
            raise Exception("Original_State: Expecting MonitoredState Input (Or Child Of)")

        if not isinstance(destination_state, MonitoredState):
            raise Exception("Destination_State: Expecting MonitoredState Input (Or Child Of)")

        always_truc_condition = AlwaysTrueCondition()
        conditional_transition = ConditionalTransition(condition=always_truc_condition,
                                                       next_state=destination_state)
        original_state.add_transition(conditional_transition)
        return conditional_transition.condition

    @staticmethod
    def _purple_link(expectedValue, original_state: 'RobotState', destination_state: 'RobotState',
                     remotecontrol: 'RemoteControl'):
        if not isinstance(original_state, RobotState):
            raise Exception("Original_State: Expecting RobotState Input")

        if not isinstance(destination_state, RobotState):
            raise Exception("Destination_State: Expecting RobotState Input")

        if remotecontrol.__class__.__name__ != "Remote":
            raise Exception("RemoteControl: Expecting ", remotecontrol.__class__.__name__, " Input")

        # if not isinstance(remotecontrol, Remote):
        #     raise Exception("L'intrant remotecontrol n'est pas de type easysensors.Remote")
        # la validation d'entré de expected value se fait dans la remote_value_condition

        remote_value_condition = RemoteValueCondition(expectedValue, remotecontrol)
        remote_transition = RemoteControlTransition(remote_value_condition, destination_state, remotecontrol)
        original_state.add_transition(remote_transition)


##     ## #### ##     ## #########    ###    ##     ##          #######
###    ##  ##  ##     ## ##          ## ##   ##     ##         ##     ##
####   ##  ##  ##     ## ##         ##   ##  ##     ##                ##
## ##  ##  ##  ##     ## #######   ##     ## ##     ##          #######
##   ####  ##   ##   ##  ##        ######### ##     ##         ##
##    ###  ##    ## ##   ##        ##     ## ##     ##         ##
##     ## ####    ###    ######### ##     ##  #######          #########


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
            raise Exception("Condition: Expecting Condition Input")

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
            raise Exception("New_Condition: Expecting Condition Input")
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
        if isinstance(condition, Condition):
            if isinstance(next_state, RobotState):
                if remote_control.__class__.__name__ != "Remote":
                    raise Exception("Remote_Control: Expecting ", remote_control.__class__.__name__, " Input")

                # if not isinstance(remote_control, easysensors.Remote):
                #    raise Exception("L'intrant remotecontrol n'est pas de type easysensors.Remote")
                self._remote_control = remote_control

                super().__init__(condition, next_state)
                # todo: bouncing
            else:
                raise Exception("Next_State: Expecting RobotState Input")
        else:
            raise Exception("Condition: Expecting Condition Input")


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
            raise Exception("Inverse: Expecting Bool Input")
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
            raise Exception("Inverse: Expecting Bool Input")
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
            raise Exception("Initial_Value: Expecting Value Not None")
        if expected_value is None:
            raise Exception("Expected_Value: Expecting Value Not None")
        if not isinstance(inverse, bool):
            raise Exception("Inverse: Expecting Bool Input")
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
            raise Exception("Duration: Expecting Float Input")
        if not isinstance(time_reference, float):
            raise Exception("Time_Reference: Expecting Float Input")
        if not isinstance(inverse, bool):
            raise Exception("Inverse: Expecting Bool Input")

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
            raise Exception("New_Duration: Expecting Float Input")

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
            raise Exception("Inverse: Expecting Bool Input")
        super().__init__(inverse)
        self._conditions: list[Condition] = []

    def add_condition(self, condition: 'Condition'):
        if not isinstance(condition, Condition):
            raise Exception("Condition: Expecting Condition Input")
        self._conditions.append(condition)

    def add_conditions(self, condition_list: ConditionList):
        if not isinstance(condition_list, list):
            raise Exception("Condition_List: Expecting List Input")
        for condition in condition_list:
            if not isinstance(condition, Condition):
                raise Exception("Error: At Least One Element Of Condition_List Is Not A Condition")
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
            raise Exception("Inverse: Expecting Bool Input")
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
            raise Exception("Inverse: Expecting Bool Input")
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
            raise Exception("Inverse: Expecting Bool Input")
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
            raise Exception("Monitored_State: Expecting MonitoredState Input")
        if not isinstance(inverse, bool):
            raise Exception("Inverse: Expecting Bool Input")

    @property
    def monitered_state(self) -> 'MonitoredState':
        return self._monitered_state

    @monitered_state.setter
    def monitered_state(self, next_monitered_state: 'MonitoredState'):
        if isinstance(next_monitered_state, MonitoredState):
            self._monitered_state = next_monitered_state
        else:
            raise Exception("Monitored_State: Expecting MonitoredState Input")


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
            raise Exception("Monitored_State: Expecting MonitoredState Input")
        if not isinstance(duration, float):
            raise Exception("Duration: Expecting Float Input")
        if not isinstance(inverse, bool):
            raise Exception("Inverse: Expecting Bool Input")

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
            raise Exception("New_Duration: Expecting Float Input")


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
            raise Exception("Monitored_State: Expecting MonitoredState Input")
        if not isinstance(expected_count, int):
            raise Exception("Expected_Count: Expecting Integer Input")
        if not isinstance(inverse, bool):
            raise Exception("Inverse: Expecting Bool Input")
        if not isinstance(auto_reset, bool):
            raise Exception("Auto_Reset: Expecting Bool Input")

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
            raise Exception("New_Expected_Count: Expecting Integer Input")


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
            raise Exception("Monitored_State: Expecting MonitoredState Input")
        if not isinstance(inverse, bool):
            raise Exception("Inverse: Expecting Bool Input")
        if expected_value is None:
            raise Exception("Expected_Value: Expecting Value Not None")

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
            raise Exception("New_Expected_Value: Expecting Value Not None")

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
    lastreading = None
    lastreadingchecked = False

    def __init__(self, expected_value: str, remote_control: 'RemoteControl' = None, inverse: bool = False):
        self._remote_control = remote_control
        self.__keycodes = ['', 'up', 'left', 'ok', 'right', 'down', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*',
                           '0', '#']
        if expected_value in self.__keycodes:
            self.__expected_value = expected_value
        else:
            raise Exception("Keycodes: Expecting Valid Keycode")
        if not isinstance(inverse, bool):
            raise Exception("Inverse: Expecting Bool Input")
        if remote_control.__class__.__name__ != "Remote":
            raise Exception("Remote_Control: Expecting ", remotecontrol.__class__.__name__, " Input")

        # if not isinstance(remote_control, easysensors.Remote):
        #    raise Exception("L'intrant remotecontrol n'est pas de type easysensors.Remote")

        super().__init__(inverse)

    def _compare(self) -> bool:
        newreading = self._remote_control.get_remote_code()
        # debounce
        if newreading != RemoteValueCondition.lastreading:
            RemoteValueCondition.lastreading = newreading
            RemoteValueCondition.lastreadingchecked = False

        if newreading == self.__expected_value:
            if RemoteValueCondition.lastreadingchecked:
                return False
            else:
                RemoteValueCondition.lastreadingchecked = True
                return True
        else:
            return False

    @property
    def expected_value(self) -> str:
        return self.__expected_value

    @expected_value.setter
    def expected_value(self, new_expected_value: str):
        if new_expected_value in self.__keycodes:
            self.__expected_value = new_expected_value
        else:
            raise Exception("New_Expected_Value: Expecting Valid Keycode")


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
            raise Exception("Action: Expecting Action (Callable) Input")


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
            raise Exception("Action: Expecting Action (Callable) Input")

    def add_in_state_action(self, action: 'Callable') -> None:
        if isinstance(action, Callable):
            self.__in_state_action.append(action)
        else:
            raise Exception("Action: Expecting Action (Callable) Input")

    def add_exiting_action(self, action: 'Callable') -> None:
        if isinstance(action, Callable):
            self.__exiting_actions.append(action)
        else:
            raise Exception("Action: Expecting Action (Callable) Input")


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


##     ## #### ##     ## #########    ###    ##     ##          #######
###    ##  ##  ##     ## ##          ## ##   ##     ##         ##     ##
####   ##  ##  ##     ## ##         ##   ##  ##     ##                ##
## ##  ##  ##  ##     ## #######   ##     ## ##     ##          #######
##   ####  ##   ##   ##  ##        ######### ##     ##                ##
##    ###  ##    ## ##   ##        ##     ## ##     ##         ##     ##
##     ## ####    ###    ######### ##     ##  #######           #######


StateGenerator = Callable[[], MonitoredState]


class Blinker(FiniteStateMachine):
    def __init__(self, off_state_generator: 'StateGenerator',
                 on_state_generator: 'StateGenerator') -> None:
        layout = FiniteStateMachine.Layout()
        self.__off = off_state_generator()
        self.__on = on_state_generator()
        self.__off_duration = off_state_generator()
        self.__on_duration = on_state_generator()
        self.__blink_on = on_state_generator()
        self.__blink_off = off_state_generator()
        self.__blink_stop_off = off_state_generator()
        self.__blink_stop_on = on_state_generator()
        self.__blink_begin = MonitoredState()
        self.__blink_stop_begin = MonitoredState()
        self.__blink_stop_end = MonitoredState()

        self.__off_duration_to_on = self._green_link(self.__off_duration,
                                                     self.__on)

        self.__on_duration_to_off = self._green_link(original_state=self.__on_duration,
                                                     destination_state=self.__off)

        self.__blink_on_to_blink_off = self._green_link(original_state=self.__blink_on,
                                                        destination_state=self.__blink_off)
        self.__blink_off_to_blink_on = self._green_link(original_state=self.__blink_off,
                                                        destination_state=self.__blink_on)

        self.__blink_begin_to_blink_off = self._orange_link(original_state=self.__blink_begin,
                                                            destination_state=self.__blink_off,
                                                            expected_value=False
                                                            )
        self.__blink_begin_to_blink_on = self._orange_link(original_state=self.__blink_begin,
                                                           destination_state=self.__blink_on,
                                                           expected_value=True)

        self.__blink_stop_off_to_blink_stop_end = self._doted_green_link(original_state=self.__blink_stop_off,
                                                                         destination_state=self.__blink_stop_end,
                                                                         ownerState=self.__blink_stop_begin)
        self.__blink_stop_on_to_blink_stop_end = self._doted_green_link(original_state=self.__blink_stop_on,
                                                                        destination_state=self.__blink_stop_end,
                                                                        ownerState=self.__blink_stop_begin)

        self.__blink_stop_off_to_blink_stop_on = self._green_link(original_state=self.__blink_stop_off,
                                                                  destination_state=self.__blink_stop_on)

        self.__blink_stop_on_to_blink_stop_off = self._green_link(original_state=self.__blink_stop_on,
                                                                  destination_state=self.__blink_stop_off)

        self.__blink_stop_begin_to_blink_stop_off = self._orange_link(original_state=self.__blink_stop_begin,
                                                                      destination_state=self.__blink_stop_off,
                                                                      expected_value=False
                                                                      )
        self.__blink_stop_begin_to_blink_stop_on = self._orange_link(original_state=self.__blink_stop_begin,
                                                                     destination_state=self.__blink_stop_on,
                                                                     expected_value=True)

        self.__blink_stop_end_to_off = self._orange_link(original_state=self.__blink_stop_end,
                                                         destination_state=self.__off,
                                                         expected_value=False
                                                         )
        self.__blink_stop_end_to_on = self._orange_link(original_state=self.__blink_stop_end,
                                                        destination_state=self.__on,
                                                        expected_value=True)

        layout.initial_state = self.__off
        layout.add_state(self.__off)
        layout.add_state(self.__on)
        layout.add_state(self.__off_duration)
        layout.add_state(self.__on_duration)
        layout.add_state(self.__blink_on)
        layout.add_state(self.__blink_off)
        layout.add_state(self.__blink_stop_off)
        layout.add_state(self.__blink_stop_on)
        layout.add_state(self.__blink_begin)
        layout.add_state(self.__blink_stop_begin)
        layout.add_state(self.__blink_stop_end)
        super().__init__(layout)

    @property
    def is_on(self) -> bool:
        return self.current_applicative_state.custom_value == True

    @property
    def is_off(self) -> bool:
        return self.current_applicative_state.custom_value == False

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
        if percent_on <= 1.0:
            if isinstance(cycle_duration, float):
                if isinstance(begin_on, bool):
                    self.__blink_begin.custom_value = begin_on
                    self.__blink_off_to_blink_on.duration = cycle_duration * percent_on
                    self.__blink_on_to_blink_off.duration = cycle_duration - (cycle_duration * percent_on)
                    self.transit_to(self.__blink_begin)
                else:
                    raise Exception("Begin_On: Expecting Bool Input")
            else:
                raise Exception("Cycle_Duration: Expecting Float Input")
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def blink2(self,
               total_duration: float,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if percent_on <= 1.0:
            if isinstance(total_duration, float):
                if isinstance(cycle_duration, float):
                    if isinstance(begin_on, bool):
                        if isinstance(end_off, bool):
                            self.__blink_stop_begin.custom_value = begin_on
                            self.__blink_stop_end.custom_value = end_off

                            self.__blink_stop_off_to_blink_stop_on.duration = cycle_duration * percent_on
                            self.__blink_stop_on_to_blink_stop_off.duration = cycle_duration - (
                                        cycle_duration * percent_on)

                            self.__blink_stop_off_to_blink_stop_end.duration = total_duration
                            self.__blink_stop_on_to_blink_stop_end.duration = total_duration

                            self.transit_to(self.__blink_stop_begin)
                        else:
                            raise Exception("End_Off: Expecting Bool Input")
                    else:
                        raise Exception("Begin_On: Expecting Bool Input")
                else:
                    raise Exception("Cycle_Duration: Expecting Float Input")
            else:
                raise Exception("Total_Duration: Expecting Float Input")
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def blink3(self,
               total_duration: float,
               n_cycle: int,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if percent_on <= 1.0:
            if isinstance(n_cycle, int):
                if isinstance(total_duration, float):
                    if isinstance(begin_on, bool):
                        if isinstance(end_off, bool):
                            self.__blink_stop_begin.custom_value = begin_on
                            self.__blink_stop_end.custom_value = end_off

                            self.__blink_stop_on_to_blink_stop_end.duration = total_duration
                            self.__blink_stop_off_to_blink_stop_end.duration = total_duration

                            self.__blink_stop_off_to_blink_stop_on.duration = (total_duration / n_cycle) * percent_on
                            self.__blink_stop_on_to_blink_stop_off.duration = (total_duration / n_cycle) - (
                                    (total_duration / n_cycle) * percent_on)

                            self.transit_to(self.__blink_stop_begin)
                        else:
                            raise Exception("End_Off: Expecting Bool Input")
                    else:
                        raise Exception("Begin_On: Expecting Bool Input")
                else:
                    raise Exception("Total_Duration: Expecting Float Input")
            else:
                raise Exception("N_Cycle: Expecting Integer Input")
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def blink4(self,
               n_cycle: int,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if percent_on <= 1.0:
            if isinstance(n_cycle, int):
                if isinstance(cycle_duration, float):
                    if isinstance(begin_on, bool):
                        if isinstance(end_off, bool):
                            self.__blink_stop_begin.custom_value = begin_on
                            self.__blink_stop_end.custom_value = end_off

                            self.__blink_stop_on_to_blink_stop_end.duration = n_cycle * cycle_duration
                            self.__blink_stop_off_to_blink_stop_end.duration = n_cycle * cycle_duration

                            self.__blink_stop_off_to_blink_stop_on = cycle_duration * percent_on
                            self.__blink_stop_on_to_blink_stop_off = cycle_duration - (cycle_duration * percent_on)

                            self.transit_to(self.__blink_stop_begin)
                        else:
                            raise Exception("End_Off: Expecting Bool Input")
                    else:
                        raise Exception("Begin_On: Expecting Bool Input")
                else:
                    raise Exception("Cycle_Duration: Expecting Float Input")
            else:
                raise Exception("N_Cycle: Expecting Integer Input")
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")


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
        self.__left_blinker = Blinker(left_off_state_generator, left_on_state_generator)
        self.__right_blinker = Blinker(right_off_state_generator, right_on_state_generator)

    def is_on(self, side: Side) -> bool:
        if isinstance(side, SideBlinkers.Side):
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
        else:
            raise Exception("Side: Expecting SideBlinker.Side Input")

    def is_off(self, side: Side) -> bool:
        if isinstance(side, SideBlinkers.Side):
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
        else:
            raise Exception("Side: Expecting SideBlinkers.Side Input")

    def turn_off(self, side: Side) -> None:
        if isinstance(side, SideBlinkers.Side):
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
        else:
            raise Exception("Side: Expecting SideBlinkers.Side Input")

    def turn_on(self, side: Side) -> None:
        if isinstance(side, SideBlinkers.Side):
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
        else:
            raise Exception("Side: Expecting SideBlinkers.Side Input")

    def turn_off2(self, side: Side, duration: float) -> None:
        if isinstance(side, SideBlinkers.Side):
            if isinstance(duration, float):
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
            else:
                raise Exception("Duration: Expecting Float Input")
        else:
            raise Exception("Side: Expecting SideBlinkers.Side Input")

    def turn_on2(self, side: Side, duration: float) -> None:
        if isinstance(side, SideBlinkers.Side):
            if isinstance(duration, float):
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
            else:
                raise Exception("Duration: Expecting Float Input")
        else:
            raise Exception("Side: Expecting SideBlinkers.Side Input")

    def blink1(self, side: Side,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True):
        if percent_on <= 1.0:
            if isinstance(side, SideBlinkers.Side):
                if isinstance(cycle_duration, float):
                    if isinstance(begin_on, bool):
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
                    else:
                        raise Exception("Begin_On: Expecting Bool Input")
                else:
                    raise Exception("Cycle_Duration: Expecting Float Input")
            else:
                raise Exception("Side: Expecting SideBlinkers.Side Input")
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def blink2(self, side: Side,
               total_duration: float,
               cycle_duration: float = 1,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if percent_on <= 1.0:
            if isinstance(side, SideBlinkers.Side):
                if isinstance(total_duration, float):
                    if isinstance(cycle_duration, float):
                        if isinstance(begin_on, bool):
                            if isinstance(end_off, bool):
                                if side == SideBlinkers.Side.LEFT:
                                    self.__left_blinker.blink2(total_duration,
                                                               cycle_duration, percent_on, begin_on, end_off)
                                elif side == SideBlinkers.Side.RIGHT:
                                    self.__right_blinker.blink2(total_duration,
                                                                cycle_duration, percent_on, begin_on, end_off)
                                elif side == SideBlinkers.Side.BOTH:
                                    self.__left_blinker.blink2(total_duration,
                                                               cycle_duration, percent_on, begin_on, end_off)
                                    self.__right_blinker.blink2(total_duration,
                                                                cycle_duration, percent_on, begin_on, end_off)
                                elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
                                    self.__left_blinker.blink2(total_duration,
                                                               cycle_duration, percent_on, begin_on, not end_off)
                                    self.__right_blinker.blink2(total_duration,
                                                                cycle_duration, percent_on, not begin_on, end_off)
                                elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
                                    self.__left_blinker.blink2(total_duration,
                                                               cycle_duration, percent_on, not begin_on, end_off)
                                    self.__right_blinker.blink2(total_duration,
                                                                cycle_duration, percent_on, begin_on, not end_off)
                            else:
                                raise Exception("End_Off: Expecting Bool Input")
                        else:
                            raise Exception("Begin_On: Expecting Bool Input")
                    else:
                        raise Exception("Cycle_Duration: Expecting Float Input")
                else:
                    raise Exception("Total_Duration: Expecting Float Input")
            else:
                raise Exception("Side: Expecting SideBlinkers.Side Input")
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def blink3(self, side: Side,
               total_duration: float,
               n_cycle: int,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if percent_on <= 1.0:
            if isinstance(side, SideBlinkers.Side):
                if isinstance(total_duration, float):
                    if isinstance(n_cycle, int):
                        if isinstance(begin_on, bool):
                            if isinstance(end_off, bool):
                                if side == SideBlinkers.Side.LEFT:
                                    self.__left_blinker.blink3(total_duration, n_cycle, percent_on, begin_on, end_off)
                                elif side == SideBlinkers.Side.RIGHT:
                                    self.__right_blinker.blink3(total_duration, n_cycle, percent_on, begin_on, end_off)
                                elif side == SideBlinkers.Side.BOTH:
                                    self.__left_blinker.blink3(total_duration, n_cycle, percent_on, begin_on, end_off)
                                    self.__right_blinker.blink3(total_duration, n_cycle, percent_on, begin_on, end_off)
                                elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
                                    self.__left_blinker.blink3(total_duration, n_cycle, percent_on, begin_on,
                                                               not end_off)
                                    self.__right_blinker.blink3(total_duration, n_cycle, percent_on, not begin_on,
                                                                end_off)
                                elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
                                    self.__left_blinker.blink3(total_duration, n_cycle, percent_on, not begin_on,
                                                               end_off)
                                    self.__right_blinker.blink3(total_duration, n_cycle, percent_on, begin_on,
                                                                not end_off)
                            else:
                                raise Exception("End_Off: Expecting Bool Input")
                        else:
                            raise Exception("Begin_On: Expecting Bool Input")
                    else:
                        raise Exception("N_Cycle: Expecting Integer Input")
                else:
                    raise Exception("Total_Duration: Expecting Float Input")
            else:
                raise Exception("Side: Expecting SideBlinkers.Side Input")
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def blink4(self,
               side: Side,
               n_cycle: int,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if percent_on <= 1.0:
            if isinstance(side, SideBlinkers.Side):
                if isinstance(n_cycle, int):
                    if isinstance(cycle_duration, float):
                        if isinstance(begin_on, bool):
                            if isinstance(end_off, bool):
                                if side == SideBlinkers.Side.LEFT:
                                    self.__left_blinker.blink4(n_cycle,
                                                               cycle_duration, percent_on, begin_on, end_off)
                                elif side == SideBlinkers.Side.RIGHT:
                                    self.__right_blinker.blink4(n_cycle,
                                                                cycle_duration, percent_on, begin_on, end_off)
                                elif side == SideBlinkers.Side.BOTH:
                                    self.__left_blinker.blink4(n_cycle,
                                                               cycle_duration, percent_on, begin_on, end_off)
                                    self.__right_blinker.blink4(n_cycle,
                                                                cycle_duration, percent_on, begin_on, end_off)
                                elif side == SideBlinkers.Side.LEFT_RECIPROCAL:
                                    self.__left_blinker.blink4(n_cycle,
                                                               cycle_duration, percent_on, begin_on, not end_off)
                                    self.__right_blinker.blink4(n_cycle,
                                                                cycle_duration, percent_on, not begin_on, end_off)
                                elif side == SideBlinkers.Side.RIGHT_RECIPROCAL:
                                    self.__left_blinker.blink4(n_cycle,
                                                               cycle_duration, percent_on, not begin_on, end_off)
                                    self.__right_blinker.blink4(n_cycle,
                                                                cycle_duration, percent_on, begin_on, not end_off)
                            else:
                                raise Exception("End_Off: Expecting Bool Input")
                        else:
                            raise Exception("Begin_On: Expecting Bool Input")
                    else:
                        raise Exception("Cycle_Duration: Expecting Float Input")
                else:
                    raise Exception("N_Cycle: Expecting Integer Input")
            else:
                raise Exception("Side: Expecting SideBlinkers.Side Input")
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def track(self) -> None:
        self.__left_blinker.track()
        self.__right_blinker.track()


##     ## #### ##     ## #########    ###    ##     ##         ########   #######  ########   #######  #########
###    ##  ##  ##     ## ##          ## ##   ##     ##         ##     ## ##     ## ##     ## ##     ##     ##
####   ##  ##  ##     ## ##         ##   ##  ##     ##         ##     ## ##     ## ##     ## ##     ##     ##
## ##  ##  ##  ##     ## #######   ##     ## ##     ##         #######   ##     ## ########  ##     ##     ##
##   ####  ##   ##   ##  ##        ######### ##     ##         ##   ##   ##     ## ##     ## ##     ##     ##
##    ###  ##    ## ##   ##        ##     ## ##     ##         ##    ##  ##     ## ##     ## ##     ##     ##
##     ## ####    ###    ######### ##     ##  #######          ##     ##  #######  ########   #######      ##


class LedBlinkers(SideBlinkers):
    def __init__(self, robot):
        self.__robot = robot
        super().__init__(lambda: LedBlinkers.LedOffLeftState(self.__robot),
                         lambda: LedBlinkers.LedOnLeftState(self.__robot),
                         lambda: LedBlinkers.LedOffRightState(self.__robot),
                         lambda: LedBlinkers.LedOnRightState(self.__robot))

    class LedOnLeftState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            # if isinstance(a_robot, Robot):
            if isinstance(parameters, State.Parameters):
                super().__init__(a_robot, parameters)
                self.custom_value = True
            else:
                raise Exception("Parameters: Expecting State.Parameters Input")

        # else:
        # raise Exception("A_Robot: Expecting Robot Input")

        def _do_entering_action(self) -> None:
            self._robot.led_on(1)

    class LedOffLeftState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            # if isinstance(a_robot, Robot):
            if isinstance(parameters, State.Parameters):
                super().__init__(a_robot, parameters)
                self.custom_value = False
            else:
                raise Exception("Parameters: Expecting State.Parameters Input")

        # else:
        # raise Exception("A_Robot: Expecting Robot Input")

        def _do_entering_action(self) -> None:
            self._robot.led_off(1)

    class LedOnRightState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            # if isinstance(a_robot, Robot):
            if isinstance(parameters, State.Parameters):
                super().__init__(a_robot, parameters)
                self.custom_value = True
            else:
                raise Exception("Parameters: Expecting State.Parameters Input")

        # else:
        # raise Exception("A_Robot: Expecting Robot Input")

        def _do_entering_action(self) -> None:
            self._robot.led_on(0)

    class LedOffRightState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            # if isinstance(a_robot, Robot):
            if isinstance(parameters, State.Parameters):
                super().__init__(a_robot, parameters)
                self.custom_value = False
            else:
                raise Exception("Parameters: Expecting State.Parameters Input")

        # else:
        # raise Exception("A_Robot: Expecting Robot Input")

        def _do_entering_action(self) -> None:
            self._robot.led_off(0)


class EyeBlinkers(SideBlinkers):
    def __init__(self, a_robot):
        # if isinstance(a_robot, Robot):
        self._robot = a_robot
        super().__init__(lambda: EyeBlinkers.EyeOffLeftState(self._robot),
                         lambda: EyeBlinkers.EyeOnLeftState(self._robot),
                         lambda: EyeBlinkers.EyeOffRightState(self._robot),
                         lambda: EyeBlinkers.EyeOnRightState(self._robot))
        # else:
        #   raise Exception("A_Robot: Expecting Robot Input")

    class EyeOnLeftState(RobotState):
        def __init__(self, a_robot, parameters: 'State.Parameters' = State.Parameters()):
            #  if isinstance(a_robot, Robot):
            if isinstance(parameters, State.Parameters):
                super().__init__(a_robot, parameters)
                self.custom_value = True
                self.couleur = (255, 0, 0)
            else:
                raise Exception("Parameters: Expecting State.Parameters Input")

        # else:
        #    raise Exception("A_Robot: Expecting Robot Input")

        def _do_entering_action(self) -> None:
            self._robot.open_left_eye()

    class EyeOffLeftState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            # if isinstance(a_robot, Robot):
            if isinstance(parameters, State.Parameters):
                super().__init__(a_robot, parameters)
                self.custom_value = False
                self.couleur = (255, 0, 0)
            else:
                raise Exception("Parameters: Expecting State.Parameters Input")

        # else:
        #   raise Exception("A_Robot: Expecting Robot Input")

        def _do_entering_action(self) -> None:
            self._robot.close_left_eye()

    class EyeOnRightState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            # if isinstance(a_robot, Robot):
            if isinstance(parameters, State.Parameters):
                super().__init__(a_robot, parameters)
                self.custom_value = True
                self.couleur = (255, 0, 0)
            else:
                raise Exception("Parameters: Expecting State.Parameters Input")

        # else:
        #   raise Exception("A_Robot: Expecting Robot Input")

        def _do_entering_action(self) -> None:
            self._robot.open_right_eye()

    class EyeOffRightState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            # if isinstance(a_robot, Robot):
            if isinstance(parameters, State.Parameters):
                super().__init__(a_robot, parameters)
                self.custom_value = False
                self.couleur = (255, 0, 0)
            else:
                raise Exception("Parameters: Expecting State.Parameters Input")

        # else:
        #   raise Exception("A_Robot: Expecting Robot Input")

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
        if isinstance(couleur, tuple):
            if isinstance(side, SideBlinkers.Side):
                if side == SideBlinkers.Side.LEFT:
                    self.set_left_eye_color(couleur)
                    self.open_left_eye()
                elif side == SideBlinkers.Side.RIGHT:
                    self.set_right_eye_color(couleur)
                    self.open_right_eye()
                elif side == SideBlinkers.Side.BOTH:
                    self.set_eye_color(couleur)
                    self.open_eyes()
            else:
                raise Exception("Side: Expecting SideBlinkers.Side Input")
        else:
            raise Exception("Couleur: Expecting Tuple (RGB) Input")

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

    def drive_cm(self, dist: float, blocking: bool = True) -> None:
        if isinstance(dist, float):
            if isinstance(blocking, bool):
                self.__robot.drive_cm(dist, blocking)
            else:
                raise Exception("Blocking: Expecting Bool Input")
        else:
            raise Exception("Dist: Expecting Float Input")

    def drive_inches(self, dist: float, blocking: bool = True) -> None:
        if isinstance(dist, float):
            if isinstance(blocking, bool):
                self.__robot.drive_inches(dist, blocking)
            else:
                raise Exception("Blocking: Expecting Bool Input")
        else:
            raise Exception("Dist: Expecting Float Input")

    def drive_degrees(self, degrees: float, blocking: bool = True) -> None:
        if isinstance(degrees, float):
            if isinstance(blocking, bool):
                return self.__robot.drive_degrees(degrees, blocking)
            else:
                raise Exception("Blocking: Expecting Bool Input")
        else:
            raise Exception("Degrees: Expecting Float Input")

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
        if isinstance(left_percent, int):
            if isinstance(right_percent, int):
                self.__robot.steer(left_percent, right_percent)
            else:
                raise Exception("Right_Percent: Expecting Integer Input between -100 and 100")
        else:
            raise Exception("Left_Percent: Expecting Integer Input between -100 and 100")

    def orbit(self, degrees: int, radius_cm: int = 0, blocking: bool = True) -> None:
        if isinstance(degrees, int):
            if isinstance(radius_cm, int):
                if isinstance(blocking, bool):
                    return self.__robot.orbit(degrees, radius_cm, blocking)
                else:
                    raise Exception("Blocking: Expecting Bool Input")
            else:
                raise Exception("Radius_Cm: Expecting Integer Input")
        else:
            raise Exception("Degrees: Expecting Integer Input between 0 and 360")

    def target_reached(self, left_target_degrees: int, right_target_degrees: int) -> bool:
        if isinstance(left_target_degrees, int):
            if isinstance(right_target_degrees, int):
                return self.__robot.target_reached(left_target_degrees, right_target_degrees)
            else:
                raise Exception("Right_Target_Degrees: Expecting Integer Input between 0 and 360")
        else:
            raise Exception("Left_Target_Degrees: Expecting Integer Input between 0 and 360")

    def reset_encoders(self, blocking: bool = True) -> None:
        if isinstance(blocking, bool):
            return self.__robot.reset_encoders(blocking)
        else:
            raise Exception("Blocking: Expecting Bool Input")

    def read_encoders_average(self, units: str = "cm") -> float:
        if isinstance(units, str):
            return self.robot.read_encoders_average(units)
        else:
            raise Exception("Units: Expecting String Input of 'cm' or 'in'")

    def turn_degrees(self, degrees: int, blocking: bool = True) -> None:
        if isinstance(degrees, int):
            if isinstance(blocking, bool):
                self.turn_degrees(degrees, blocking)
            else:
                raise Exception("Blocking: Expecting Bool Input")
        else:
            raise Exception("Degrees: Expecting Integer Input between 0 and 360")

    def blinker_on(self, id: int) -> None:
        if isinstance(id, int):
            self.__robot.blinker_on(id)
        else:
            raise Exception("Id: Expecting Integer Input of 0 (Right Blinker) or 1 (Left Blinker)")

    def blinker_off(self, id: int) -> None:
        if isinstance(id, int):
            self.__robot.blinker_off(id)
        else:
            raise Exception("Id: Expecting Integer Input of 0 (Right Blinker) or 1 (Left Blinker)")

    def led_on(self, id: int) -> None:
        if isinstance(id, int):
            self.__robot.led_on(id)
        else:
            raise Exception("Id: Expecting Integer Input of 0 (Right LED) or 1 (Left LED)")

    def led_off(self, id: int) -> None:
        if isinstance(id, int):
            self.__robot.led_off(id)
        else:
            raise Exception("Id: Expecting Integer Input of 0 (Right LED) or 1 (Left LED)")

    def set_left_eye_color(self, color: tuple) -> None:
        if isinstance(color, tuple):
            self.__robot.set_left_eye_color(color)
        else:
            raise Exception("Color: Expecting Tuple (RGB) Input")

    def set_right_eye_color(self, color: tuple) -> None:
        if isinstance(color, tuple):
            self.__robot.set_right_eye_color(color)
        else:
            raise Exception("Color: Expecting Tuple (RGB) Input")

    def set_eye_color(self, color: tuple) -> None:
        if isinstance(color, tuple):
            self.__robot.set_eye_color(color)
        else:
            raise Exception("Color: Expecting Tuple (RGB) Input")

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

    def init_light_sensor(self, port: str = "AD1") -> 'LightSensor':
        if isinstance(port, str):
            return self.__robot.init_light_sensor(port)
        else:
            raise Exception("Port: Expecting String Input of 'AD1'")

    def init_sound_sensor(self, port: str = "AD1") -> 'SoundSensor':
        if isinstance(port, str):
            return self.__robot.init_sound_sensor(port)
        else:
            raise Exception("Port: Expecting String Input of 'AD1'")

    def init_loudness_sensor(self, port: str = "AD1"):
        if isinstance(port, str):
            return self.__robot.init_loudness_sensor(port)
        else:
            raise Exception("Port: Expecting String Input of 'AD1'")

    def init_ultrasonic_sensor(self, port: str = "AD1"):
        if isinstance(port, str):
            return self.__robot.init_ultrasonic_sensor(port)
        else:
            raise Exception("Port: Expecting String Input of 'AD1'")

    def init_buzzer(self, port: str = "AD1"):
        if isinstance(port, str):
            return self.__robot.init_buzzer(port)
        else:
            raise Exception("Port: Expecting String Input of 'AD1'")

    def init_led(self, port: str = "AD2"):
        if isinstance(port, str):
            return self.__robot.init_led(port)
        else:
            raise Exception("Port: Expecting String Input of 'AD2'")

    def init_button_sensor(self, port: str = "AD1"):
        if isinstance(port, str):
            return self.__robot.init_button_sensor(port)
        else:
            raise Exception("Port: Expecting String Input of 'AD1'")

    def init_line_follower(self, port: str = "I2C"):
        if isinstance(port, str):
            return self.__robot.init_line_follower(port)
        else:
            raise Exception("Port: Expecting String Input of 'I2C'")

    def init_servo(self, port: str = "SERVO1"):
        if isinstance(port, str):
            return self.__robot.init_servo(port)
        else:
            raise Exception("Port: Expecting String Input of 'SERV01'")

    def init_distance_sensor(self, port: str = "I2C"):
        if isinstance(port, str):
            return self.__robot.init_distance_sensor(port)
        else:
            raise Exception("Port: Expecting String Input of 'I2C'")

    def init_light_color_sensor(self, port: str = "I2C", led_state: bool = True):
        if isinstance(port, str):
            if isinstance(led_state, bool):
                return self.__robot.init_light_color_sensor(port, led_state)
            else:
                raise Exception("Led_State: Expecting Bool Input")
        else:
            raise Exception("Port: Expecting String Input of 'I2C'")

    def init_imu_sensor(self, port: str = "I2C"):
        if isinstance(port, str):
            return self.__robot.init_imu_sensor(port)
        else:
            raise Exception("Port: Expecting String Input of 'I2C'")

    def init_dht_sensor(self, sensor_type: int = 0):
        if isinstance(sensor_type, int):
            return self.__robot.init_dht_sensor(sensor_type)
        else:
            raise Exception("Sensor_Type: Expecting Integer Input of 0 (Blue DHT Sensor) or 1 (White DHT Sensor)")

    def init_remote(self, port: str = "AD1"):
        if isinstance(port, str):
            return self.__robot.init_remote(port)
        else:
            raise Exception("Port: Expecting String Input of 'AD1'")

    def init_motion_sensor(self, port: str = "AD1"):
        if isinstance(port, str):
            return self.__robot.init_motion_sensor(port)
        else:
            raise Exception("Port: Expecting String Input of 'AD1'")


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
        self.__home.add_entering_action(lambda: print("home"))

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
        self.__task1.add_in_state_action(lambda: self.__task1_state_action)

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

    def __task1_state_action(self):
        print("state action task1")
        self.__task1.track()

    def track(self) -> bool:
        self._robot.eye_blinkers.track()
        self._robot.led_blinkers.track()
        if isinstance(self.current_applicative_state, ManualControl):
            self.__task1.track()
        return super().track()


class ManualControl(RobotState):

    def track(self):
        self.fsm.track()

    class StopState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            if isinstance(robot, Robot):
                if isinstance(parameters, State.Parameters):
                    super().__init__(robot, parameters)
                    self.custom_value = 'stop'
                else:
                    raise Exception("Parameters: Expecting State.Parameters Input")
            else:
                raise Exception("Robot: Expecting Robot Input")

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.turn_off(SideBlinkers.Side.BOTH)
            self._robot.stop()

    class RotateRightState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            if isinstance(robot, Robot):
                if isinstance(parameters, State.Parameters):
                    super().__init__(robot, parameters)
                    self.custom_value = 'Right'
                else:
                    raise Exception("Parameters: Expecting State.Parameters Input")
            else:
                raise Exception("Robot: Expecting Robot Input")

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.blink1(SideBlinkers.Side.RIGHT, 1.0, 0.50, True)
            self._robot.right()

    class RotateLeftState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            if isinstance(robot, Robot):
                if isinstance(parameters, State.Parameters):
                    super().__init__(robot, parameters)
                    self.custom_value = 'Left'
                else:
                    raise Exception("Parameters: Expecting State.Parameters Input")
            else:
                raise Exception("Robot: Expecting Robot Input")

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.blink1(SideBlinkers.Side.LEFT, 1.0, 0.50, True)
            self._robot.left()

    class ForwardState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            if isinstance(robot, Robot):
                if isinstance(parameters, State.Parameters):
                    super().__init__(robot, parameters)
                    self.custom_value = 'Forward'
                else:
                    raise Exception("Parameters: Expecting State.Parameters Input")
            else:
                raise Exception("Robot: Expecting Robot Input")

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.blink1(SideBlinkers.Side.BOTH, 1.0, 0.25, True)
            self._robot.foward()

    class BackwardState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            if isinstance(robot, Robot):
                if isinstance(parameters, State.Parameters):
                    super().__init__(robot, parameters)
                    self.custom_value = 'Backward'
                else:
                    raise Exception("Parameters: Expecting State.Parameters Input")
            else:
                raise Exception("Robot: Expecting Robot Input")

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.blink1(SideBlinkers.Side.BOTH, 1.0, 0.75)
            self._robot.backward()

    def __init__(self, remoteControl: 'RemoteControl', robot: 'Robot',
                 parameters: 'State.Parameters' = State.Parameters()):
        if isinstance(robot, Robot):
            # if isinstance(remoteControl, 'RemoteControl'):
            if isinstance(parameters, State.Parameters):
                super().__init__(robot, parameters)
                self.__rotate_left = self.RotateLeftState(self._robot)
                self.__forward = self.ForwardState(self._robot)
                self.__stop = self.StopState(self._robot)
                self.__rotate_right = self.RotateRightState(self._robot)
                self.__backwards = self.BackwardState(self._robot)
                self._remote_control = remoteControl
            else:
                raise Exception("Parameters: Expecting State.Parameters Input")
        # else:
        #   raise Exception("RemoteControl: Expecting RemoteControl Input")
        else:
            raise Exception("Robot: Expecting Robot Input")

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




