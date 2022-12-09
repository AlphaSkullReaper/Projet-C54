""""La classe Transition encapsule le concept d'une transition dans le context du patron de conception 'FINITE STATE MACHINE.
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
       ...   def __init__(self, next_state: 'State' = None):
       ...      super().__init__(next_state)

       >>>  def _do_transiting_action(self):
       ...      print("Transiting action")


       >>>  def is_transiting(self) -> bool:
       >>>      return True
       >>>

       Exemple des proprités:
       -Transition.next_state(setter)
       >>> enfant_transition = EnfantTransition()
       >>> enfant_transition.next_state = State()

       -Transition.next_state(getter)
       >>> enfant_transition = EnfantTransition()
       >>> print(enfant_transition.next_state)

        -Transition.is_valid(lecture)
        >>> enfant_transition = EnfantTransition()
       >>> print(enfant_transition.is_valid)
   """

class test:
    def __init__(self):
        pass

def __main_doctest():
    import test
    doctest.testmod()  # verbose=True)


if __name__ == "__main__":
    __main_doctest()