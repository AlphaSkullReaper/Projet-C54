import doctest
from abc import abstractmethod, ABC
from enum import Enum
from time import perf_counter
from Last_Jupyter_Version import RobotState
from niveau2 import MonitoredState, StateEntryDurationCondition, ConditionalTransition, StateValueCondition, \
    AlwaysTrueCondition
from robotState import RemoteValueCondition, RemoteControlTransition


class State:
    """"
    La classe State encapsule le concept d'un état dans le context du patron de conception FINITE STATE MACHINE.

    Un état se caractérise par:
    -Un objet Parameters(classe Interne)
    -une liste de Transition

    Les fonctionalités disponibles:
    -validation de la liste de transition
    -ajout de transition
    -éxécution d'action à l'entré de l'état
    -éxécution d'action à la sortie de l'état
    -éxécution d'action de l'état
    -vérification de l'état de transition

    Comment créer un état?:
    La classe peut prendre un objet Parametre cependant celui-ci est optionel , car il se fait créer par défaut

    Les propriétés(acessuers et mutateurs sont:
    -get_transitionList(lecture)
    -is_valid(lecture)
    -is_terminal(lecture)
    -is_transiting(lecture)

    sur la classe Interne Parameters:
    Celle ci est composer de 3 variables d'instances:
    -terminal(bool)
    -do_in_state_when_entering(bool)
    -do_in_state_when_exiting(bool)

    Le bool terminal indique si l'état indique l'arrêt du FiniteStateMachine en cours(voir FiniteStateMachine) => par défault faux
    Le bool do_in_state_when_entering indique si on exécute l'action de l'état quand on rentre de l'état en plus de son action d'entrée => par défault faux
    Le bool do_in_state_when_exiting indique si on exécute l'action de l'état quand on sort de l'état en plus de son action de sortie  => par défault faux

    sur la validation d'état:
     la propriéter is_valid vérifie si il a au moins une transition dans la liste de transition et que chaque transition est valide(voir Transition)

     sur l'état des transistion:
     la proprieter is_transiting retourne la premiere transition valide.(voir Transition pour plus de détail)

     sur l'ajout de transition:
     la transition passer an argument est rajouter dans la liste de transition en variable d'instance.

     sur l'éxécutation d'action en entré:
    la fonction _do_entering_action contient tous le code à éxécuter lorsqu'on rentre dans l'état. Celle-ci se fait apeller par sa fonction exec:_exec_entering_action. Pour plus de détails sur les fonctions exec et do aller voir
    la documentation sur transition.

     sur l'éxécutation d'action en sortie:
    la fonction _do_exiting_action contient tous le code à éxécuter lorsqu'on rentre dans l'état. Celle-ci se fait apeller par sa fonction exec:_exec_exiting_action. Pour plus de détails sur les fonctions exec et do aller voir
    la documentation sur transition.

     sur l'éxécutation d'action de l'état:
    la fonction _do_in_state_action contient tous le code à éxécuter lorsqu'on rentre dans l'état. Celle-ci se fait apeller par sa fonction exec:_exec_in_state_action. Pour plus de détails sur les fonctions exec et do aller voir
    la documentation sur transition.


    >>>state = State()
    >>> state.add_transition(enfantTransition())
    >>> print(state.is_transiting)
    true
    """
    #TODO: vérifier doctest avec prof
    class Parameters:
        def __init__(self,terminal:bool = False,do_in_state_when_entering:bool = False,do_in_state_action_when_exiting:bool = False):
            self.terminal: bool = terminal
            self.do_in_state_when_entering: bool = do_in_state_when_entering
            self.do_in_state_action_when_exiting: bool = do_in_state_action_when_exiting

    def __init__(self, parameters: 'Parameters' = Parameters()) -> None:
        self.__parameters = parameters
        self.__transition: list['Transition'] = [] #TODO: validation

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




class Transition(ABC):
    """""La classe Transition encapsule le concept d'une transition dans le context du patron de conception 'FINITE STATE MACHINE.
       Celle-ci est une classe abstraite implementer par ses enfants: ConditonalTransition,ActionTransition,MonitoredTransition,RemoteTransition.
       Elle a comme rôle d'imposer les fonctionalités et les caractéristiques lister ci-dessous à tous ses enfants afin d'uniformiser l'apelle des fonctionalités
       d'une Transition à tout les niveaux du programme.

       Une transition est exprimer:
        -par un état suivant.

       Les fonctionalités disponible:
       -validation de l'état suivant
       -exécutation d'action durant la transition
       -vérifier si la transition est active

       Comment créer une transition?:
       Puisque c'est une classe abstraite, il est imposible de créer une isnstance de transition.
       Il faut créer une classe enfant pour l'utiliser voir la liste d'enfant plus haut.

       Les propriétés(acessuers et mutateurs sont:
       -Transition.next_state(lecture/écriture)
       -Transition.is_valid(lecture)

       sur la validation de l'état suivant:
           la propriéter is_valid vérifie si l'état suivant est non None.


       sur l'éxucutation d'action durant la transition:
       -il a deux fonctions responsanble de cette fonctionalité:
           -Transition._do_transiting_action
           -Transtion._exec_transiting_action
       Comme vous pouvez remarquer ces fonctions sont protéges, elles sont donc seulement acessible par les enfants.
       En premier, la fonction  _do_transiting_action contient le code à éxécuter durant la transition.Celle-ci doit être redéfinit dans la classe efant pour être utiliser
       Mais ce n'est pas tout, la fonction _exec_transiting_action apelle toujours _do_transiting_action.Cette fonction n'a pas besoin d'être réfinit, car en utilisant le conept
       de polymorphisme apelle toujours la fonction réfinit dans ses enfants.


       sur la vérification de la transition est active:
       la fonction responsable de cette fonctionalité est:
        -Transition.is_transiting
        celle ci est une fonction abstraite qui doit donc absoltement être implémenter.
        Elle doit return un bool selon les conditions qui vous mettez.


       Exemples d'usage d'implémentation de la classe abstraite:

       >>> class EnfantTransition(Transition):
       ...      def __init__(self, next_state: 'State' = None):
       ...          super().__init__(next_state)
       ...      def _do_transiting_action(self):
       ...          print("Transiting action")
       ...      def is_transiting(self) -> bool:
       ...          return True

       Exemple des proprités:
       -Transition.next_state(setter)
       >>> enfant_transition = EnfantTransition(State())
       >>> enfant_transition._exec_transiting_action()
       Transiting action

   """

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



def __main_doctest():
    import test
    doctest.testmod()  # verbose=True)


if __name__ == "__main__":
    __main_doctest()

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
            if not isinstance(new_state,State):
                raise Exception("L'intrant newState n'est pas de type State")
            if new_state.is_valid:
                self._initial_state = new_state

        def add_state(self, new_state: 'State') -> None:
            if not isinstance(new_state, State):
                raise Exception("L'intrant newState n'est pas de type State")
            if new_state.is_valid:
                self.states.append(new_state)

        def add_states(self, list_states: StateList) -> None:
            if not isinstance(list_states, list):
                raise Exception("L'intrant list_states n'est pas de type liste")
            for state in list_states:
                if not isinstance(state,State):
                    raise Exception("L'intrant list_states a au moins un élément qui n'est pas de type State")

            for a_state in list_states:
                if a_state.is_valid:
                    self.states.append(a_state)



    def __init__(self, layout_parameter: 'Layout', uninitialized: bool = True) -> None:  # do typing layount:Layount
        if not isinstance(layout_parameter,FiniteStateMachine.Layout):
            raise Exception("L'intrant layout_parameter n'est pas de type Layout")
        if not isinstance(uninitialized,bool):
            raise Exception("L'intrant uninitialized n'est pas de type bool")

        if layout_parameter.is_valid:
            self.__layout = layout_parameter
        else:
            raise Exception("Layout non valide")
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
        if not isinstance(reset,bool):
            raise Exception("L'intrant reset n'est pas de type bool")
        if not isinstance(time_budget,float):
            raise Exception("L'intrant layout_parameter n'est pas de type Layout")

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
            self.__current_applicative_state._exec_entering_action() #lien d'amitier

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
        self.__current_applicative_state._exec_entering_action()

    def transit_to(self, state: 'State') -> None:
        if not isinstance(state,State):
            raise Exception("L'intrant state n'est pas de type State")
        if self.__current_applicative_state is not None:
            self.__current_applicative_state._exec_exiting_action()
        self.__current_applicative_state = state
        self.__current_operational_state = FiniteStateMachine.OperationalState.IDLE
        self.__current_applicative_state._exec_entering_action()

    def _transit_by(self, transition: 'Transition') -> None:
        if not isinstance(transition,Transition):
            raise Exception("L'intrant transition n'est pas de type Transition")
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
        if not isinstance(original_state,MonitoredState):
            raise Exception("L'intrant original_state n'est pas de type ou enfant de MonitoredState")

        if not isinstance(destination_state,MonitoredState):
            raise Exception("L'intrant destination_state n'est pas de type ou enfant de MonitoredState")
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
            raise Exception("L'intrant original_state n'est pas de type ou enfant de MonitoredState")

        if not isinstance(destination_state, MonitoredState):
            raise Exception("L'intrant destination_state n'est pas de type ou enfant de MonitoredState")

        if not isinstance(ownerState, MonitoredState):
            raise Exception("L'intrant ownerState n'est pas de type ou enfant de MonitoredState")

        state_entry_duration_condition = StateEntryDurationCondition(duration=1.0,
                                                                     monitered_state=ownerState)
        conditional_transition = ConditionalTransition(condition=state_entry_duration_condition,
                                                       next_state=destination_state)
        original_state.add_transition(next_transition=conditional_transition)

        return conditional_transition.condition

    @staticmethod
    def _orange_link(original_state: 'MonitoredState', destination_state: 'MonitoredState', expected_value: bool):
        if not isinstance(original_state, MonitoredState):
            raise Exception("L'intrant original_state n'est pas de type ou enfant de MonitoredState")

        if not isinstance(destination_state, MonitoredState):
            raise Exception("L'intrant destination_state n'est pas de type ou enfant de MonitoredState")

        if not isinstance(expected_value, bool):
            raise Exception("L'intrant expected_value n'est pas de type ou enfant de bool")

        state_value_condition = StateValueCondition(expected_value=expected_value,
                                                    monitered_state=original_state)
        conditional_transition = ConditionalTransition(condition=state_value_condition,
                                                       next_state=destination_state)
        original_state.add_transition(conditional_transition)
        return conditional_transition.condition

    @staticmethod
    def _blue_link(original_state: 'MonitoredState', destination_state: 'MonitoredState'):
        if not isinstance(original_state, MonitoredState):
            raise Exception("L'intrant original_state n'est pas de type ou enfant de MonitoredState")

        if not isinstance(destination_state, MonitoredState):
            raise Exception("L'intrant destination_state n'est pas de type ou enfant de MonitoredState")

        always_truc_condition = AlwaysTrueCondition()
        conditional_transition = ConditionalTransition(condition=always_truc_condition,
                                                       next_state=destination_state)
        original_state.add_transition(conditional_transition)
        return conditional_transition.condition

    @staticmethod
    def purple_link(expectedValue, original_state: 'RobotState', destination_state: 'RobotState',
                    remotecontrol: 'RemoteControl'):
        if not isinstance(original_state, RobotState):
            raise Exception("L'intrant original_state n'est pas de type RobotState")

        if not isinstance(destination_state, RobotState):
            raise Exception("L'intrant destination_state n'est pas de type RobotState")

        if not isinstance(remotecontrol, easysensors.Remote):
            raise Exception("L'intrant remotecontrol n'est pas de type easysensors.Remote")
        #la validation d'entré de expected value se fait dans la remote_value_condition

        remote_value_condition = RemoteValueCondition(expectedValue, remotecontrol)
        remote_transition = RemoteControlTransition(remote_value_condition, destination_state, remotecontrol)
        original_state.add_transition(remote_transition)
