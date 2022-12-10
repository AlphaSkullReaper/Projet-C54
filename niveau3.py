from niveau1 import FiniteStateMachine
from niveau2 import MonitoredState
from enum import Enum
from typing import Callable

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
        if percent_on <= 1.0:  # TODO:validation
            self.__blink_begin.custom_value = begin_on
            self.__blink_off_to_blink_on.duration = cycle_duration * percent_on
            self.__blink_on_to_blink_off.duration = cycle_duration - (cycle_duration * percent_on)
            self.transit_to(self.__blink_begin)
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def blink2(self,
               total_duration: float,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if percent_on <= 1.0:  # TODO:validation
            self.__blink_stop_begin.custom_value = begin_on
            self.__blink_stop_end.custom_value = end_off

            self.__blink_stop_off_to_blink_stop_on.duration = cycle_duration * percent_on
            self.__blink_stop_on_to_blink_stop_off.duration = cycle_duration - (cycle_duration * percent_on)

            self.__blink_stop_off_to_blink_stop_end.duration = total_duration
            self.__blink_stop_on_to_blink_stop_end.duration = total_duration

            self.transit_to(self.__blink_stop_begin)
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def blink3(self,
               total_duration: float,
               n_cycle: int,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if percent_on <= 1.0:  # TODO:validation
            self.__blink_stop_begin.custom_value = begin_on
            self.__blink_stop_end.custom_value = end_off

            self.__blink_stop_on_to_blink_stop_end.duration = total_duration
            self.__blink_stop_off_to_blink_stop_end.duration = total_duration

            self.__blink_stop_off_to_blink_stop_on.duration = (total_duration / n_cycle) * percent_on
            self.__blink_stop_on_to_blink_stop_off.duration = (total_duration / n_cycle) - (
                    (total_duration / n_cycle) * percent_on)

            self.transit_to(self.__blink_stop_begin)
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def blink4(self,
               n_cycle: int,  # TODO:validation
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if percent_on <= 1.0:
            self.__blink_stop_begin.custom_value = begin_on
            self.__blink_stop_end.custom_value = end_off

            self.__blink_stop_on_to_blink_stop_end.duration = n_cycle * cycle_duration
            self.__blink_stop_off_to_blink_stop_end.duration = n_cycle * cycle_duration

            self.__blink_stop_off_to_blink_stop_on = cycle_duration * percent_on
            self.__blink_stop_on_to_blink_stop_off = cycle_duration - (cycle_duration * percent_on)

            self.transit_to(self.__blink_stop_begin)
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

    def is_on(self, side: Side) -> bool:  # TODO:validation
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

    def is_off(self, side: Side) -> bool:  # TODO:validation
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

    def turn_off(self, side: Side) -> None:  # TODO:validation
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

    def turn_on(self, side: Side) -> None:  # TODO:validation
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

    def turn_off2(self, side: Side, duration: float) -> None:  # TODO:validation
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

    def turn_on2(self, side: Side, duration: float) -> None:  # TODO:validation
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

    def blink1(self, side: Side,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True):  # TODO:validation
        if percent_on <= 1.0:
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
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def blink2(self, side: Side,
               total_duration: float,
               cycle_duration: float = 1,  # TODO:validation
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if percent_on <= 1.0:
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
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def blink3(self, side: Side,
               total_duration: float,
               n_cycle: int,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):  # TODO:validation
        if percent_on <= 1.0:
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
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def blink4(self,
               side: Side,
               n_cycle: int,
               cycle_duration: float = 1.0,
               percent_on: float = 0.5,
               begin_on: bool = True,
               end_off: bool = True):
        if percent_on <= 1.0:  # TODO:validation
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
        else:
            raise Exception("Percent_On: Expecting numerical value between 0 and 1.")

    def track(self) -> None:
        self.__left_blinker.track()
        self.__right_blinker.track()
