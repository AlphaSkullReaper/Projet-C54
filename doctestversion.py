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

        >>> class EnfantTransition(Transition):
        ...     def __init__(self, next_state: 'State' = None):
        ...         super().__init__(next_state)
        ...     def _do_transiting_action(self):
        ...         print("Transiting action")
        ...     def is_transiting(self) -> bool:
        ...         return True
        ...
        >>> state = State()
        >>> state.add_transition(EnfantTransition(State()))
        >>> transition = state.is_transiting
        >>> if transition is not None:
        ...     print(True)
        True
          """
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
    """
    La classe FiniteStateMachine encaspule le concept de machine d'état dans notre patron de Concpetion FINITE STATE MACHINE.
    Celle-ci à comme responsibilité de gérer les transitions entre chaque état anisi que les actions des états.

    Une machine d'état se caractérise par:
    -un layout (classe interne)
    -un état applicatif courant
    -un état opérationelle courant (classe interne)

    Les fonctionalités disponibles`:
        -run:
        -track
        -reset
        -stop
        -transit_to
        -transit_by
        -fonctions de création de transitions ainsi que leur condition(Méthode Statique):
            - _green_link
            - _doted_green_link
            - _orange_link
            - _blue_link
            -_purple_link

    Comment créer une FiniteStateMachine?:
        Le constructeur prend un layout valide et un bool uninitialized (De base à true) qui permet d'avoir l'assignation de l'état courant applicative directement dans le constructeur aini que l'état opérationelle à IDLE.

    Sur la terminologie état applicatif et état opérationelle:
        L'état applicatif fait référence à un objet de classe State tandis que l'état opérationelle est un objet de type OperationalState(voir plus bas)

    Les propriétés(acessuers et mutateurs sont:
        -current_applicative_state(lecture)
        -current_operational_state(lecture)


    Sur la fonctionalité track:
        La fonction track est le morceau le plus important de toute la classe. C'est cette fonction qui est responsable des transitions entre chaque état ainsi que de leur actions.
        Son fonctionement est le suivant. Elle vérifie en premier si la machine à état n'est pas  en état opérationelle initilisater(UNINITIALISED) si c'est  le cas alors  on assigne l'état initial comme état applicative courant contenu dans le layout et effectue l'action d'entré d'état(voir état).
        Grâce au concept de lien d'amitié,la classe peut apeller la fonctionn protéger de l'état. Le lien d'amitié permet à une classe d'accéder les fonctionilés protégé d'une classe comme si celle-ci était son enfant.Ensuite,on vérifie que notre machine n'est pas en état opérationelle terminal(TERMINAL). Si oui, alors on effecte l'action de sortie de l'état et on retourne faux.
        À partir de maintement, la machine à état atteint l'état opérationelle running et le coeur de la logique des transitions et actions d'état est effectuer comme suis.
        Si Finalement, la machine est en cours alors on vérifie si on transitione. Si c'est le cas , alors on appliqye la transition par transit by et effectue l'action d'état du nouvelle état assigner en transit_by. Si ce n'est pas le cas on effectue l'action d'état.


    Sur la fonctionalité run:
        La fonction run  apelle la fonction track tand que track n'atteint pas un état terminal(tant que track ne retourne pas faux).
        la fonction contient 2 options:
        -l'application d'un time budget c'est-à-dire une duré maximal pendant lequel la machine est en action.
        -la possibilé de reset avant de commencer l'apelle.

    Sur la fonctionality _transit_by:
        En premier cette fonction resoit une transition et vérifie si la transition pointe vers un état terminal, si c'est le cas alors on assigne l'état opérationelle terminal reached qui va ensuite être vérifier dans track.
        En deuxème, on effecte l'action de sortie de l'état courant , affectue l'action de la transition, assigne le prochaine état à l'état applicatif courant et en dernier effectue l'action d'entré du nouvelle état.

    Sur la fonctionalité stop:
       Celle-ci met l'état opérationelle à idle. Elle est utiliser dans la boucle while pour signaliser l'arrêt de la machine d'état lorsqu'on éteint un état terminal ou le time_budget est échoué.


    Sur la fonctionalité reset:
        Celle-ci remet notre état applicatif à l'état initial et nous met à l'état opréationelle Idle.

    sur la fonctionalité transit_to:
    Tout comme transit by cette fonction est responsable de gérer les transitions, mais celle si transition directement vers un état futur sans passer par une transition. C'est-à-dire qu'elle assigne
    l'état courant aplicatif est directement égal au prochaine état passer en paramêtre. Le reste de la logique est la même que transit_by.

    sur _green_link:
     permet de créer une transition avec la condition StateEntryDurationCondition. Prend un état orignal(MonitoredState), un état de distantion(MonitoredState) servant de next state. Ainsi qu'une duration.

     sur _doted_green_link:
        permet de créer une transition avec la condition StateEntryDurationCondition. Prend un état orignal(MonitoredState), un état de distantion(MonitoredState) servant de next state. Ainsi qu'une duration et un owner state.
        La transition de temps est baser sur la duré du owner state plutot que sur le original state

    sur _orange_link:
         permet de créer une transition avec la condition StateValueCondition. Prend un état orignal(MonitoredState), un état de distantion(MonitoredState) servant de next state. Ainsi qu'une expected value.

    sur _blue_link:
        permet de créer une transition avec la condition AlwaysTrueCondition. Prend un état orignal(MonitoredState), un état de distantion(MonitoredState) servant de next state.

    sur _purple_link:
     permet de créer une transition avec la condition RemoteValueCondition. Prend un état orignal(RobotState), un état de distantion(RobotState) servant de next state. une expected value étant un des 12 keycodes sur la manette et en dernier une manette.


    sur la class interne OperationalState:
        cette classe contient les 4 états représentant le fonctionement de la machine à état:
        - UNINITIALIZED : aucun état applicatif courant,machine non fonctionelle
        -IDLE : état applicatif courant valide, en attende
        -RUNNING :  machine à état fonctionne
        -TERMINAL_REACHED : point vers un état terminal

    sur la classe Interne Layout:
        celle class encapslue le concept d'un plan contenant tous les états disponibles pour la machine d'état.

    un layout est caractérisé par:
        -un tableau d'état
        - un état initial

    Les fonctionalités disponible:
        -validation du layou
        -ajout d'état unique
        -ajout d'un tableau d'état

    Les propriétés(acessuers et mutateurs sont:
       -is_valid(lecture)
       -initial_state(lecture/écriture)

    comment créer un layout et utiliser un layout?:
        le programme utilise une logique très spécifique sur la création et l'utilisation du layout:
        Cette facon consiste à un créer un loyout vide, d'y rajouter l'état initial ainsi que les autres états.
        Pour ensuite passer ce layout dans le constructeur de notre FiniteStateMachine

    sur la validation du layout:
        la layout est considérer comme valide si il contient un état intial et que chaqun des états contenu dans celui-ci soit valide.

    >>> class EnfantTransition(Transition):
    ...     def __init__(self, next_state: 'State' = None):
    ...         super().__init__(next_state)
    ...     def _do_transiting_action(self):
    ...         print("Transiting action")
    ...     def is_transiting(self) -> bool:
    ...         return True
    ...
    >>> state1 = State()
    >>> state2 = State()
    >>> state1.add_transition(EnfantTransition(state2))
    >>> state2.add_transition(EnfantTransition(state1))
    >>>
    ...
    >>> layout = FiniteStateMachine.Layout()
    >>> layout.initial_state = state1
    >>> layout.add_states([state1,state2])
    ...
    >>> MyStateMachine = FiniteStateMachine(layout)
    >>> if MyStateMachine.current_applicative_state is None:
    ...     print(True)
    True
    >>> MyStateMachine.transit_to(state2)
    >>> if MyStateMachine.current_applicative_state is not None:
    ...     print(True)
    True
    """
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
                if not isinstance(state, State):
                    raise Exception("L'intrant list_states a au moins un élément qui n'est pas de type State")

            for a_state in list_states:
                if a_state.is_valid:
                    self.states.append(a_state)



    def __init__(self, layout_parameter: 'Layout', uninitialized: bool = True) -> None:  # do typing layount:Layount
        if not isinstance(layout_parameter, FiniteStateMachine.Layout):
            raise Exception("L'intrant layout_parameter n'est pas de type Layout")
        if not isinstance(uninitialized, bool):
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
        if not isinstance(reset, bool):
            raise Exception("L'intrant reset n'est pas de type bool")

        if time_budget is not None:
            if not isinstance(time_budget, float):
                raise Exception("L'intrant time_budget n'est pas de type float")
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
            raise Exception("L'intrant state n'est pas de type State")
        if self.__current_applicative_state is not None:
            self.__current_applicative_state._exec_exiting_action()
        self.__current_applicative_state = state
        self.__current_operational_state = FiniteStateMachine.OperationalState.IDLE
        self.__current_applicative_state._exec_entering_action()

    def _transit_by(self, transition: 'Transition') -> None:
        if not isinstance(transition, Transition):
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
        if not isinstance(original_state, MonitoredState):
            raise Exception("L'intrant original_state n'est pas de type ou enfant de MonitoredState")

        if not isinstance(destination_state, MonitoredState):
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
    def _purple_link(expectedValue, original_state: 'RobotState', destination_state: 'RobotState',
                     remotecontrol: 'RemoteControl'):
        if not isinstance(original_state, RobotState):
            raise Exception("L'intrant original_state n'est pas de type RobotState")

        if not isinstance(destination_state, RobotState):
            raise Exception("L'intrant destination_state n'est pas de type RobotState")

        if remotecontrol.__class__.__name__ != "Remote":
            raise Exception("L'intrant remotecontrol n'est pas 'Remote' mais plutôt", remotecontrol.__class__.__name__)

        print("Type est: ", remotecontrol.__class__.__qualname__);
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
            raise Exception("L'intrant remotecontrol n'est pas 'Remote' mais plutôt", remote_control.__class__.__name__)

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
        self._remote_control = "test"
        self.__keycodes = ['', 'up', 'left', 'ok', 'right', 'down', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*',
                           '0', '#']
        if expected_value in self.__keycodes:
            self.__expected_value = expected_value
        else:
            raise Exception("Expected value must be a valid keycode ")
        if not isinstance(inverse, bool):
            raise Exception("L'intrant inverse n'est pas de type bool")
        #if remote_control.__class__.__name__ != "Remote":
        #    raise Exception("L'intrant remotecontrol n'est pas 'Remote' mais plutôt", remote_control.__class__.__name__)

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


##     ## #### ##     ## #########    ###    ##     ##         ########   #######  ########   #######  #########
###    ##  ##  ##     ## ##          ## ##   ##     ##         ##     ## ##     ## ##     ## ##     ##     ##
####   ##  ##  ##     ## ##         ##   ##  ##     ##         ##     ## ##     ## ##     ## ##     ##     ##
## ##  ##  ##  ##     ## #######   ##     ## ##     ##         #######   ##     ## ########  ##     ##     ##
##   ####  ##   ##   ##  ##        ######### ##     ##         ##   ##   ##     ## ##     ## ##     ##     ##
##    ###  ##    ## ##   ##        ##     ## ##     ##         ##    ##  ##     ## ##     ## ##     ##     ##
##     ## ####    ###    ######### ##     ##  #######          ##     ##  #######  ########   #######      ##

"""
class LedBlinkers(SideBlinkers):
    def __init__(self, robot):
        self.__robot = "test"
        super().__init__(lambda: LedBlinkers.LedOffLeftState(self.__robot),
                         lambda: LedBlinkers.LedOnLeftState(self.__robot),
                         lambda: LedBlinkers.LedOffRightState(self.__robot),
                         lambda: LedBlinkers.LedOnRightState(self.__robot))

    class LedOnLeftState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)  # TODO:validation
            self.custom_value = True

        def _do_entering_action(self) -> None:
            self._robot.led_on(1)

    class LedOffLeftState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)  # TODO:validation
            self.custom_value = False

        def _do_entering_action(self) -> None:
            self._robot.led_off(1)

    class LedOnRightState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)  # TODO:validation
            self.custom_value = True

        def _do_entering_action(self) -> None:
            self._robot.led_on(0)

    class LedOffRightState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)  # TODO:validation
            self.custom_value = False

        def _do_entering_action(self) -> None:
            self._robot.led_off(0)

"""

"""
class EyeBlinkers(SideBlinkers):
    def __init__(self, a_robot):
        self._robot = a_robot  # TODO:validation
        super().__init__(lambda: EyeBlinkers.EyeOffLeftState(self._robot),
                         lambda: EyeBlinkers.EyeOnLeftState(self._robot),
                         lambda: EyeBlinkers.EyeOffRightState(self._robot),
                         lambda: EyeBlinkers.EyeOnRightState(self._robot))

    class EyeOnLeftState(RobotState):
        def __init__(self, a_robot, parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)  # TODO:validation
            self.custom_value = True
            self.couleur = (255, 0, 0)

        def _do_entering_action(self) -> None:
            self._robot.open_left_eye()

    class EyeOffLeftState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)
            self.custom_value = False  # TODO:validation
            self.couleur = (255, 0, 0)

        def _do_entering_action(self) -> None:
            self._robot.close_left_eye()

    class EyeOnRightState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)  # TODO:validation
            self.custom_value = True
            self.couleur = (255, 0, 0)

        def _do_entering_action(self) -> None:
            self._robot.open_right_eye()

    class EyeOffRightState(RobotState):
        def __init__(self, a_robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(a_robot, parameters)
            self.custom_value = False  # TODO:validation
            self.couleur = (255, 0, 0)

        def _do_entering_action(self) -> None:
            self._robot.close_right_eye()
"""


"""
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
        if side == SideBlinkers.Side.LEFT:
            self.set_left_eye_color(couleur)  # TODO:validation
            self.open_left_eye()
        elif side == SideBlinkers.Side.RIGHT:
            self.set_right_eye_color(couleur)
            self.open_right_eye()
        elif side == SideBlinkers.Side.BOTH:
            self.set_eye_color(couleur)
            self.open_eyes()

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

    def drive_cm(self, dist: float, blocking: bool = True) -> None:  # TODO:validation
        self.__robot.drive_cm(dist, blocking)

    def drive_inches(self, dist: float, blocking: bool = True) -> None:  # TODO:validation
        self.__robot.drive_inches(dist, blocking)

    def drive_degrees(self, degrees: float, blocking: bool = True):  # TODO: Check return without follow up
        return self.__robot.drive_degrees(degrees, blocking)  # TODO:validation

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
        self.__robot.steer(left_percent, right_percent)  # TODO:validation

    def orbit(self, degrees: int, radius_cm: int = 0, blocking: bool = True):  # TODO: Check return without follow up
        return self.__robot.orbit(degrees, radius_cm, blocking)  # TODO:validation

    def target_reached(self, left_target_degrees: int, right_target_degrees: int) -> bool:
        return self.__robot.target_reached(left_target_degrees, right_target_degrees)  # TODO:validation

    def reset_encoders(self, blocking: bool = True) -> None:
        return self.__robot.reset_encoders(blocking)  # TODO:validation

    def read_encoders_average(self, units: str = "cm") -> float:
        return self.robot.read_encoders_average(units)  # TODO:validation

    def turn_degrees(self, degrees: int, blocking: bool = True) -> None:
        self.turn_degrees(degrees, blocking)  # TODO:validation

    def blinker_on(self, id: int) -> None:
        self.__robot.blinker_on(id)  # TODO:validation

    def blinker_off(self, id: int) -> None:
        self.__robot.blinker_off(id)  # TODO:validation

    def lef_on(self, id: int) -> None:
        self.__robot.led_on(id)  # TODO:validation

    def lef_off(self, id: int) -> None:
        self.__robot.led_off(id)  # TODO:validation

    def set_left_eye_color(self, color: tuple) -> None:
        self.__robot.set_left_eye_color(color)  # TODO:validation

    def set_right_eye_color(self, color: tuple) -> None:
        self.__robot.set_right_eye_color(color)  # TODO:validation

    def set_eye_color(self, color: tuple) -> None:
        self.__robot.set_eye_color(color)  # TODO:validation

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

    def init_light_sensor(self, port: str = "AD1"):  # TODO check return easysensors.LightSensor
        return self.__robot.init_light_sensor(port)  # TODO:validation

    def init_sound_sensor(self, port: str = "AD1"):  # TODO easysensors.SoundSensor
        return self.__robot.init_sound_sensor(port)  # TODO:validation

    def init_loudness_sensor(self, port: str = "AD1"):
        return self.__robot.init_loudness_sensor(port)  # TODO:validation

    def init_ultrasonic_sensor(self, port: str = "AD1"):
        return self.__robot.init_ultrasonic_sensor(port)  # TODO:validation

    def init_buzzer(self, port: str = "AD1"):
        return self.__robot.init_buzzer(port)  # TODO:validation

    def init_led(self, port: str = "AD2"):
        return self.__robot.init_led(port)  # TODO:validation

    def init_button_sensor(self, port: str = "AD1"):
        return self.__robot.init_button_sensor(port)  # TODO:validation

    def init_line_follower(self, port: str = "I2C"):
        return self.__robot.init_line_follower(port)  # TODO:validation

    def init_servo(self, port: str = "SERVO1"):
        return self.__robot.init_servo(port)  # TODO:validation

    def init_distance_sensor(self, port: str = "I2C"):
        return self.__robot.init_distance_sensor(port)  # TODO:validation

    def init_light_color_sensor(self, port: str = "I2C", led_state=True):
        return self.__robot.init_light_color_sensor(port)  # TODO:validation

    def init_imu_sensor(self, port: str = "I2C"):
        return self.__robot.init_imu_sensor(port)  # TODO:validation

    def init_dht_sensor(self, sensor_type: int = 0):
        return self.__robot.init_dht_sensor(sensor_type)  # TODO:validation

    def init_remote(self, port: str = "AD1"):
        return self.__robot.init_remote(port)  # TODO:validation

    def init_motion_sensor(self, port: str = "AD1"):
        return self.__robot.init_motion_sensor(port)
"""
"""
class C64Project(FiniteStateMachine):
    def __init__(self):
        self._robot = "Robert Robot"
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

    def track(self) -> bool:
        self._robot.eye_blinkers.track()
        self._robot.led_blinkers.track()
        self.__task1.track()
        return super().track()
"""

"""
class ManualControl(RobotState):

    def track(self):
        self.fsm.track()

    class StopState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(robot, parameters)  # TODO:validation
            self.custom_value = 'stop'

        def _do_entering_action(self) -> None:
            print(self._robot.led_blinkers.is_on(SideBlinkers.Side.BOTH))
            if self.entry_count > 1:
                self._robot.led_blinkers.turn_off(SideBlinkers.Side.BOTH)
            self._robot.stop()

    class RotateRightState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(robot, parameters)  # TODO:validation
            self.custom_value = 'Right'

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.blink1(SideBlinkers.Side.RIGHT, 1.0, 0.50, True)
            self._robot.right()

    class RotateLeftState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(robot, parameters)  # TODO:validation
            self.custom_value = 'Left'

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.blink1(SideBlinkers.Side.LEFT, 1.0, 0.50, True)
            self._robot.left()

    class ForwardState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(robot, parameters)  # TODO:validation
            self.custom_value = 'Forward'

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.blink1(SideBlinkers.Side.BOTH, 1.0, 0.25, True)
            self._robot.foward()

    class BackwardState(RobotState):
        def __init__(self, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
            super().__init__(robot, parameters)  # TODO:validation
            self.custom_value = 'Backward'

        def _do_entering_action(self) -> None:
            self._robot.led_blinkers.blink1(SideBlinkers.Side.BOTH, 1.0, 0.75)
            self._robot.backward()

    def __init__(self, remoteControl, robot: 'Robot', parameters: 'State.Parameters' = State.Parameters()):
        super().__init__(robot, parameters)  # TODO:validation
        self.__rotate_left = self.RotateLeftState(self._robot)
        self.__forward = self.ForwardState(self._robot)
        self.__stop = self.StopState(self._robot)
        self.__rotate_right = self.RotateRightState(self._robot)
        self.__backwards = self.BackwardState(self._robot)
        self._remote_control = remoteControl

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

"""


#c64 = C64Project()
#c64.run()


if __name__ == "__main__":
   import doctest
   doctest.testmod()


