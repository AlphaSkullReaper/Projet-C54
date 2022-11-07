from ActionState import ActionState
from State import State
from time import perf_counter
from abc import abstractmethod


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
        val = perf_counter()
        self.__counter_last_entry = val
        self.__counter_last_exit = val

    @abstractmethod
    def exec_entering_action(self) -> None:
        self.__counter_last_entry = perf_counter()
        self.__entry_count += 1
        super()._do_entering_action()

    @abstractmethod
    def exec_exiting_action(self) -> None:
        super()._do_exiting_action()
        self.__counter_last_exit = perf_counter()
