from typing import Optional
from math import (sqrt, tau, sin, cos, acos, atan2, degrees, radians,
                  isclose, trunc, ceil, floor)
from random import uniform


class Vect2D:
    """La classe Vect2D encapsule les notions d'un vecteur mathÃ©matique.

    Le vecteur est exprimÃ© selon :

    - un espace Ã  deux dimensions
    - un systÃ¨me de coordonnÃ©es cartÃ©siennes
    - deux nombres rÃ©els (float) :
        - x, les abscisses
        - y, les ordonnÃ©es

    Plusieurs fonctionnalitÃ©s sont disponibles :

    - propriÃ©tÃ©s et caractÃ©ristiques
    - reprÃ©sentation cartÃ©sienne et polaire
    - surcharge des opÃ©rateurs
    - vecteur unitaire
    - comparaison entre 2 vecteurs : angle, distance, perpendicularitÃ©, ...
    - produits, projections et rÃ©jections
        - scalaire
        - vectoriel
    - plusieurs fonctions utilitaires :
        - assignations diverses et rÃ©initialisation
        - arrondissements
        - valeur absolue
        - distances
    - gÃ©nÃ©ration alÃ©atoire

    Il existe plusieurs faÃ§ons de **crÃ©er** un `Vect2D` :

    - `Vect2D()`
    - `Vect2D.from_vect2d`
    - `Vect2D.from_polar`
    - `Vect2D.from_polar_degrees`
    - `Vect2D.from_random_normalized`
    - `Vect2D.from_random_cartesian`
    - `Vect2D.from_random_polar`
    - `Vect2D.from_random_polar_degrees`
    - `Vect2D.from_data`

    Les **propriÃ©tÃ©s** (accesseurs et mutateurs) sont :

    - `Vect2D.is_defined` [lecture] : retourne vrai si le vecteur est dÃ©fini
    - `Vect2D.is_normalized` [lecture] : retourne vrai si le vecteur est de longueur 1
    - `Vect2D.x` [lecture/Ã©criture] : l'abscisse de la coordonnÃ©e cartÃ©sienne
    - `Vect2D.y` [lecture/Ã©criture] : l'ordonnÃ©e de la coordonnÃ©e cartÃ©sienne
    - `Vect2D.length` [lecture/Ã©criture] : la longueur de la coordonnÃ©e polaire
    - `Vect2D.length_squared` [lecture/Ã©criture] : la longueur au carrÃ© de la coordonnÃ©e polaire
    - `Vect2D.orientation` [lecture/Ã©criture] : l'orientation de la coordonnÃ©e polaire en radians
    - `Vect2D.orientation_degrees` [lecture/Ã©criture] : l'orientation de la coordonnÃ©e polaire en degrÃ©es
    - `Vect2D.normalized` [lecture] : retourne vrai si le vecteur est unitaire
    - `Vect2D.right_perpendicular` [lecture] : retourne le vecteur perpendiculaire de droite
    - `Vect2D.left_perpendicular` [lecture] : retourne le vecteur perpendiculaire de gauche
    - `Vect2D.flipped` [lecture] : retourne le vecteur permutÃ©
    - `Vect2D.manhattan_length` [lecture] : retourne la distance de Mannhatan
    - `Vect2D.chebyshev_length` [lecture] : retourne la distance de Chebyshev
    - `Vect2D.as_tuple` [lecture] : retourne un tuple de deux rÃ©els
    - `Vect2D.as_list` [lecture] : retourne une liste de deux rÃ©els
    - `Vect2D.as_dict` [lecture] : retourne un dictionnaire de deux rÃ©els avec 'x' et 'y' comme clÃ©s

    Pour le systÃ¨me de coordonnÃ©es **cartÃ©siennes** :

    - `Vect2D`
    - `Vect2D.x`
    - `Vect2D.y`
    - `Vect2D.clamp_x`
    - `Vect2D.clamp_y`

    Pour le systÃ¨me de coordonnÃ©es **polaires** :

    - `Vect2D.from_polar`
    - `Vect2D.set_polar`
    - `Vect2D.length_squared`
    - `Vect2D.length`
    - `Vect2D.orientation`
    - `Vect2D.limit_length_squared`
    - `Vect2D.limit_length`

    Pour la **normalisation** (unitaire) :

    - `Vect2D.is_normalized`
    - `Vect2D.normalize`
    - `Vect2D.normalized`

    Pour la **gÃ©nÃ©ration alÃ©atoire** :

    - `Vect2D.randomize_normalized`
    - `Vect2D.randomize_cartesian`
    - `Vect2D.randomize_polar`
    - `Vect2D.from_random_normalized`
    - `Vect2D.from_random_cartesian`
    - `Vect2D.from_random_polar`
    - `Vect2D.from_random_polar_degrees`

    **Comparaison** de deux vecteurs :

    - `Vect2D.distance_squared_from`
    - `Vect2D.distance_from`
    - `Vect2D.is_perpendicular_to`
    - `Vect2D.is_parallel_to`
    - `Vect2D.angle_between`
    - `Vect2D.angle_disparity`
    - `Vect2D.is_forming_accute_angle_with`
    - `Vect2D.is_forming_obtuse_angle_with`

    **Produits** et **projection** entre 2 vecteurs :

    - `Vect2D.dot`
    - `Vect2D.cross`
    - `Vect2D.scalar_projection`
    - `Vect2D.vector_projection`
    - `Vect2D.scalar_rejection`
    - `Vect2D.vector_rejection`
    - `Vect2D.projection_analysis`

    **Surcharge** des **opÃ©rateurs** et **fonctions** standards de `Python` (`v` pour vecteur et `s` pour scalaire) :

    - Comparaison entre 2 vecteurs :
        - `v1 == v2`
        - `v1 != v2`
        - ne modifie pas les vecteurs
        - retourne un `bool`
    - Inverse d'un vecteur :
        - `-v`
        - ne modifie pas le vecteur
        - retourne une nouvelle instance de `Vect2D`
    - Addition ou soustraction de 2 vecteurs :
        - `v1 + v2`
        - `v1 - v2`
        - ne modifie pas les vecteurs
        - retourne une nouvelle instance de `Vect2D`
    - Addition ou soustraction avec assignation de 2 vecteurs :
        - `v1 += v2`
        - `v1 -= v2`
        - modifie l'instance de gauche sans modifier l'instance de droite
        - retourne l'instance de gauche
    - Multiplicationt ou division entre 1 vecteur et 1 scalaire :
        - `v * s`
        - `s * v`
        - `v / s`
        - `s / v`
        - ne modifie pas le vecteur ou le scalaire
        - retourne une nouvelle instance de `Vect2D`
    - Multiplicationt ou division avec assignation entre 1 vecteur et 1 scalaire :
        - `v *= s`
        - `v /= s`
        - modifie l'instance de gauche (le vecteur) sans modifier l'instance de droite (le scalaire)
        - retourne l'instance de gauche (le vecteur)
    - Fonctions d'arrondissement
        - toutes ces fonction :
            - ne modifie pas l'instance passÃ©e
            - retourne une nouvelle instance de `Vect2D`
            - les valeur `x` et `y` restent des `float` mÃªme si elles sont arrondies
        - `round(v)`
            - affectue l'arrondissement de `x` et de `y` vers l'entier le plus prÃ¨s
        - `trunc(v)`
            - affectue une arrondissement de `x` et de `y` vers zÃ©ro
        - `floor(v)`
            - affectue une arrondissement de `x` et de `y` vers l'infini nÃ©gatif
        - `ceil(v)`
            - affectue une arrondissement de `x` et de `y` vers l'infini positif
    - Autres fonctions utilitaires
        - `abs(v)`
            - ne modifie pas l'instance passÃ©e
            - retourne une nouvelle instance de `Vect2D`
            - valeure absolue de `x` et de `y`
        - `complex(v)`
            - ne modifie pas l'instance passÃ©e
            - retourne un nombre complexe reprÃ©sentant le vecteur

    **Conversion** vers un type externe et utilitaires :

    - Conversion :
        - `bool(v)` :
            - retourne un boolÃ©en vrai si le vecteur est dÃ©fini
        - `repr(v)` :
            - retourne une chaÃ®ne de caractÃ¨res technique
        - `str(v)` :
            - retourne une chaÃ®ne de caractÃ¨res descriptive
            - les fonctions suivantes permettent de paramÃ©triser la conversion
                - `Vect2D.set_string_format`
                - `Vect2D.set_value_format`
        - `Vect2D.as_tuple` :
            - retourne un tuple de deux rÃ©els
        - `Vect2D.as_list` :
            - retourne une liste de deux rÃ©els
        - `Vect2D.as_dict` :
            - retourne un dictionnaire de deux rÃ©els

    Le vecteur est aussi un **itÃ©rateur** :

    - l'itÃ©rateur pointe vers l'instance originale et reste une _vue_ de ce
      vecteur

    Exemples d'usage avec un itÃ©rateur :

        >>> v1 = Vect2D(1.0, -2.5)
        >>> for coord in v1:
        ...     print(coord)
        1.0
        -2.5
        >>> i = iter(v1)
        >>> print(next(i))
        1.0
        >>> v1.y = 100.0
        >>> print(next(i))
        100.0
    """

    __slots__ = ('x', 'y')

    def __clamp(min_value: int | float, value: int | float, max_value: int | float) -> int | float:
        return max(min_value, min(value, max_value))

    # -------------------------------------------
    #     ____                _   _
    #    / ___|_ __ ___  __ _| |_(_) ___  _ __
    #   | |   | '__/ _ \/ _` | __| |/ _ \| '_ \
    #   | |___| | |  __/ (_| | |_| | (_) | | | |
    #    \____|_|  \___|\__,_|\__|_|\___/|_| |_|
    #
    # -------------------------------------------
    def __init__(self, x: int | float = 0., y: int | float = 0.) -> None:
        """CrÃ©ation d'un objet `Vect2D` utilisant le systÃ¨me de coordonnÃ©es cartÃ©siennes.

        Args:
            x (int | float): La valeur des abscisse. Defaults = 0.0
            y (int | float): La valeur des ordonnÃ©es. Defaults = 0.0

        Exemples:
            >>> vect = Vect2D()
            >>> print(vect)
            (0.00E+00, 0.00E+00)
            >>> vect = Vect2D(-1.0, 1.0)
            >>> print(vect)
            (-1.00E+00, 1.00E+00)
        """
        self.x: float = float(x)
        """`Read & Write`

        La valeur des abscisses selon le systÃ¨me de coordonnÃ©es cartÃ©siennes.

        Exemples:
            >>> v1 = Vect2D()
            >>> v1.x = 5.0
            >>> print(v1)
            (5.00E+00, 0.00E+00)
        """
        self.y: float = float(y)
        """`Read & Write`

        La valeur des ordonnÃ©es selon le systÃ¨me de coordonnÃ©es cartÃ©siennes.

        Exemples:
            >>> v1 = Vect2D()
            >>> v1.y = -5.0
            >>> print(v1)
            (0.00E+00, -5.00E+00)
        """

    @classmethod
    def from_vect2d(cls, other: 'Vect2D') -> 'Vect2D':
        """CrÃ©ation un nouvel objet `Vect2D` identique Ã  un autre.

        Args:
            other (Vect2D): Le vecteur Ã  cloner.

        Exemples:
            >>> v1 = Vect2D(-1.0, 1.0)
            >>> v2 = Vect2D.from_vect2d(v1)
            >>> print(v2)
            (-1.00E+00, 1.00E+00)
        """
        return cls(other.x, other.y)

    # -----------------------------------------------------------------------------------
    #    ____  _        _                                                 _
    #   / ___|| |_ _ __(_)_ __   __ _    ___ ___  _ ____   _____ _ __ ___(_) ___  _ __
    #   \___ \| __| '__| | '_ \ / _` |  / __/ _ \| '_ \ \ / / _ \ '__/ __| |/ _ \| '_ \
    #    ___) | |_| |  | | | | | (_| | | (_| (_) | | | \ V /  __/ |  \__ \ | (_) | | | |
    #   |____/ \__|_|  |_|_| |_|\__, |  \___\___/|_| |_|\_/ \___|_|  |___/_|\___/|_| |_|
    #                           |___/
    # -----------------------------------------------------------------------------------

    __string_prefix = '('
    __string_separator = ', '
    __string_suffix = ')'
    __string_use_scientific_notation = True
    __string_trailing_zeros_length = 2
    __string_value_format = '.2E'

    @staticmethod
    def set_string_format(prefix: str = None, separator: str = None, suffix: str = None) -> None:
        """DÃ©termine le format du texte lors de la conversion vers une chaÃ®ne
        de caractÃ¨res : prÃ©fixe, sÃ©parateur et suffixe.

        Args:
            prefix (str): Le text prÃ©cÃ©dant la coordonnÃ©es x. Si None, le prÃ©fixe reste inchangÃ©. Defaults = None
            separator (str): Le texte entre les coordonnÃ©es x et y. Si None, le sÃ©parator est laissÃ© inchangÃ©. Defaults = None
            suffix (str): le texte aprÃ¨s la coordonnÃ©es y. Si None, le suffixe est laissÃ© inchangÃ©. Defaults = None

        Exemples:
            >>> vect = Vect2D(20000.0, 3.141592654)
            >>> print(vect)
            (2.00E+04, 3.14E+00)
            >>> Vect2D.set_string_format('[[[ ', ' : ', ' ]]]')
            >>> print(vect)
            [[[ 2.00E+04 : 3.14E+00 ]]]
            >>> Vect2D.set_string_format('(', ', ', ')')
        """
        if prefix: Vect2D.__string_prefix = prefix
        if separator: Vect2D.__string_separator = separator
        if suffix: Vect2D.__string_suffix = suffix

    @staticmethod
    def set_value_format(use_scientific_notation: Optional[bool] = None,
                         trailing_zeros_length: Optional[int] = None) -> None:
        """DÃ©termine le format des rÃ©els lors de la conversoin vers une chaÃ®ne
        de caractÃ¨res : la reprÃ©sentation des nombres rÃ©els x et y.

        Args:
            use_scientific_notation (bool): Si True, utilise la notation scientifique. Si False, la notation fixe. Si None, la notation reste inchangÃ©e. Defaults = None
            trailing_zeros_length (int): DÃ©termine le nombre de 0 aprÃ¨s la virgule. Si None, le 'padding' reste inchangÃ©. Defaults = None

        Exemples:
            >>> vect = Vect2D(20000.0, 3.141592654)
            >>> print(vect)
            (2.00E+04, 3.14E+00)
            >>> Vect2D.set_value_format(False, 3)
            >>> print(vect)
            (20000.000, 3.142)
            >>> Vect2D.set_value_format(True, 2)
        """
        use_scientific_notation = Vect2D.__string_use_scientific_notation if use_scientific_notation is None else use_scientific_notation
        trailing_zeros_length = Vect2D.__string_trailing_zeros_length if trailing_zeros_length is None else trailing_zeros_length
        Vect2D.__string_value_format = f'.{trailing_zeros_length}{"E" if use_scientific_notation else "f"}'

    def __repr__(self) -> str:
        """Retourne une chaÃ®ne de caractÃ¨res contenant une reprÃ©sentation
        technique de du vecteur.

        Exemples:
            >>> v1 = Vect2D(2.0, -2.0)
            >>> print(repr(v1))
            vect2d.Vect2D(x=2.0, y=-2.0)
        """
        return f'vect2d.Vect2D(x={self.x}, y={self.y})'

    def __str__(self) -> str:
        """Retourne une chaÃ®ne de caractÃ¨res reprÃ©sentant le vecteur.

        Cette reprÃ©sentation est paramÃ©trÃ©e par les fonctions :
         - set_string_format
         - set_value_format

        Exemples:
            >>> v1 = Vect2D(2.0, -2.0)
            >>> print(v1)
            (2.00E+00, -2.00E+00)
        """
        return f'{Vect2D.__string_prefix}{self.x:{Vect2D.__string_value_format}}{Vect2D.__string_separator}{self.y:{Vect2D.__string_value_format}}{Vect2D.__string_suffix}'

    class __Vect2D_Iter:
        def __init__(self, vect2d: 'Vect2D'):
            self.__vect2d = vect2d
            self.__i = 0

        def __next__(self):
            if self.__i == 0:
                self.__i += 1
                return self.__vect2d.x
            if self.__i == 1:
                self.__i += 1
                return self.__vect2d.y
            else:
                raise StopIteration

    def __iter__(self):
        """
        >>> v1 = Vect2D(2.0, -1.5)
        >>> tu = tuple(v1)
        >>> li = list(v1)
        >>> print(tu)
        (2.0, -1.5)
        >>> print(li)
        [2.0, -1.5]
        """
        return Vect2D.__Vect2D_Iter(self)

    # --------------------------------------
    #     ____                           _
    #    / ___| ___ _ __   ___ _ __ __ _| |
    #   | |  _ / _ \ '_ \ / _ \ '__/ _` | |
    #   | |_| |  __/ | | |  __/ | | (_| | |
    #    \____|\___|_| |_|\___|_|  \__,_|_|
    #
    # --------------------------------------

    def __bool__(self) -> bool:
        """Conversion du vecteur vers un boolÃ©en en effectuant une validation
        du vecteur. Le vecteur est valide s'il est dÃ©fini.

        Exemples:
            >>> v1 = Vect2D(2.0, 0.0)
            >>> print('ok' if v1 else 'failed')
            ok
            >>> v1.reset()
            >>> print('ok' if v1 else 'failed')
            failed
        """
        return self.is_defined

    @property
    def is_defined(self) -> bool:
        """`Read only`

        Retourne `True` si le vecteur est dÃ©fini, `False` autrement. Un vecteur
        indÃ©fini est un vecteur de longueur 0.

        Exemples:
            >>> v1 = Vect2D(2.0, 0.0)
            >>> v1.is_defined
            True
            >>> v1.reset()
            >>> v1.is_defined
            False
        """
        return not (isclose(self.x, 0.) and isclose(self.y, 0.))

    # ---------------------------------------------------------------
    #       _            _                                  _
    #      / \   ___ ___(_) __ _ _ __  _ __ ___   ___ _ __ | |_ ___
    #     / _ \ / __/ __| |/ _` | '_ \| '_ ` _ \ / _ \ '_ \| __/ __|
    #    / ___ \\__ \__ \ | (_| | | | | | | | | |  __/ | | | |_\__ \
    #   /_/   \_\___/___/_|\__, |_| |_|_| |_| |_|\___|_| |_|\__|___/
    #                      |___/
    # ---------------------------------------------------------------

    def copy(self) -> 'Vect2D':
        """Retourne une copie (deepcopy) du vecteur.

        Exemples:
            >>> v1 = Vect2D(3.14, 2.81)
            >>> v2 = v1.copy()
            >>> print(v2)
            (3.14E+00, 2.81E+00)
        """
        return Vect2D(self.x, self.y)

    def copy_from(self, other: 'Vect2D') -> None:
        """Copie les coordonnÃ©es x et y d'un vecteur source vers celui-ci.

        Args:
            other (Vect2D): Le vecteur source.

        Exemples:
            >>> v1 = Vect2D()
            >>> v2 = Vect2D(-2.0, 1.5)
            >>> v1.copy_from(v2)
            >>> print(v1)
            (-2.00E+00, 1.50E+00)
        """
        self.x, self.y = other.x, other.y

    def copy_to(self, other: 'Vect2D') -> None:
        """Copie les coordonnÃ©es courantes x et y vers un autre vecteur.

        Args:
            other (Vect2D): Le vecteur cible.

        Exemples:
            >>> v1 = Vect2D()
            >>> v2 = Vect2D(2.0, -1.5)
            >>> v2.copy_to(v1)
            >>> print(v1)
            (2.00E+00, -1.50E+00)
        """
        other.x, other.y = self.x, self.y

    def set(self, x: int | float, y: int | float) -> None:
        """DÃ©termine les valeurs x et y.

        Args:
            x (float | int): La coordonnÃ©es en x.
            y (float | int): La coordonnÃ©es en y.

        Exemples:
            >>> v1 = Vect2D()
            >>> v1.set(-2.0, -1.5)
            >>> print(v1)
            (-2.00E+00, -1.50E+00)
        """
        self.x, self.y = float(x), float(y)

    def reset(self) -> None:
        """RÃ©initialise le vecteur (0.0, 0.0). Le vecteur est indÃ©fini.

        Exemples:
            >>> v1 = Vect2D(2.0, 1.5)
            >>> print(v1)
            (2.00E+00, 1.50E+00)
            >>> v1.reset()
            >>> print(v1)
            (0.00E+00, 0.00E+00)
        """
        self.x, self.y = 0., 0.

    # ------------------------------------------------------------------------------------------------------
    #     ____           _            _                                       _ _             _
    #    / ___|__ _ _ __| |_ ___  ___(_) __ _ _ __     ___ ___   ___  _ __ __| (_)_ __   __ _| |_ ___  ___
    #   | |   / _` | '__| __/ _ \/ __| |/ _` | '_ \   / __/ _ \ / _ \| '__/ _` | | '_ \ / _` | __/ _ \/ __|
    #   | |__| (_| | |  | ||  __/\__ \ | (_| | | | | | (_| (_) | (_) | | | (_| | | | | | (_| | ||  __/\__ \
    #    \____\__,_|_|   \__\___||___/_|\__,_|_| |_|  \___\___/ \___/|_|  \__,_|_|_| |_|\__,_|\__\___||___/
    #
    # ------------------------------------------------------------------------------------------------------
    def clamp_x(self, x_min: float, x_max: float) -> None:
        """Borne l'abscisse entre deux limites.

        Args:
            x_min (float): La borne infÃ©rieure.
            x_max (float): La borne supÃ©rieure.

        Exemples:
            >>> v1 = Vect2D(2.0, 0.0)
            >>> v1.clamp_x(2.5, 5.0)
            >>> print(v1)
            (2.50E+00, 0.00E+00)
        """
        self.x = Vect2D.__clamp(x_min, self.x, x_max)

    def clamp_y(self, y_min: float, y_max: float) -> None:
        """Borne l'ordonnÃ©e entre deux limites.

        Args:
            y_min (float): La borne infÃ©rieure.
            y_max (float): La borne supÃ©rieure.

        Exemples:
            >>> v1 = Vect2D(2.0, 0.0)
            >>> v1.clamp_y(5.0, 10.0)
            >>> print(v1)
            (2.00E+00, 5.00E+00)
        """
        self.y = Vect2D.__clamp(y_min, self.y, y_max)

    @property
    def manhattan_length(self) -> float:
        """`Read only`

        Retourne la distance de Manhattan.

        Cette distance correspond Ã  la distance orthogonale totale Ã  parcourir
        considÃ©rant chacun des axes : | x | + | y |.

        Exemples:
            >>> v1 = Vect2D(2.0, 5.0)
            >>> v1.manhattan_length
            7.0
        """
        return abs(self.x) + abs(self.y)

    @property
    def chebyshev_length(self) -> float:
        """`Read only`

        Retourne la distance de Chebyshev.

        Cette distance correspond Ã  la distance la plus grande entre les
        abscisses et les ordonnÃ©es.

        Exemples:
            >>> v1 = Vect2D(2.0, 5.0)
            >>> v1.chebyshev_length
            5.0
        """
        return max(abs(self.x), abs(self.y))

    def minkowski_length(self, order: float = 2.) -> float:
        """Retourne la distance de Minkowski.

        Args:
            order (float): Le coefficient de puissance utilisÃ©. Defaults = 2.0

        Exemples:
            >>> v1 = Vect2D(2.0, 1.0)
            >>> v1.minkowski_length(1)
            3.0
        """
        return (abs(self.x) ** order + abs(self.y) ** order) ** (1. / order)

    @property
    def right_perpendicular(self) -> 'Vect2D':
        """`Read only`

        Retourne une nouvelle instance de 'Vect2D' reprÃ©sentant une rotation
        de 90Â° vers la droite.

        Exemples:
            >>> v1 = Vect2D(2.0, 1.0)
            >>> print(v1.right_perpendicular)
            (1.00E+00, -2.00E+00)
        """
        return Vect2D(self.y, -self.x)

    @property  # getter only
    def left_perpendicular(self) -> 'Vect2D':  # name ?
        """`Read only`

        Retourne une nouvelle instance de 'Vect2D' reprÃ©sentant une rotation
        de 90Â° vers la gauche.

        Exemples:
            >>> v1 = Vect2D(2.0, 1.0)
            >>> print(v1.left_perpendicular)
            (-1.00E+00, 2.00E+00)
        """
        return Vect2D(-self.y, self.x)

    @property
    def flipped(self) -> 'Vect2D':
        """`Read only`

        Retourne une nouvelle instance de 'Vect2D' ayant les coordonnÃ©es
        permutÃ©es.

        Exemples:
            >>> v1 = Vect2D(2.0, 5.0)
            >>> print(v1.flipped)
            (5.00E+00, 2.00E+00)
        """
        return Vect2D(self.y, self.x)

    def flip(self) -> None:
        """Permute les valeurs x et y.

        Exemples:
            >>> v1 = Vect2D(2.0, 5.0)
            >>> v1.flip()
            >>> print(v1)
            (5.00E+00, 2.00E+00)
        """
        self.x, self.y = self.y, self.x

    # -----------------------------------------------------------------------------------
    #    ____       _                                      _ _             _
    #   |  _ \ ___ | | __ _ _ __    ___ ___   ___  _ __ __| (_)_ __   __ _| |_ ___  ___
    #   | |_) / _ \| |/ _` | '__|  / __/ _ \ / _ \| '__/ _` | | '_ \ / _` | __/ _ \/ __|
    #   |  __/ (_) | | (_| | |    | (_| (_) | (_) | | | (_| | | | | | (_| | ||  __/\__ \
    #   |_|   \___/|_|\__,_|_|     \___\___/ \___/|_|  \__,_|_|_| |_|\__,_|\__\___||___/
    #
    # -----------------------------------------------------------------------------------

    @classmethod
    def from_polar(cls, length: float, orientation: float) -> 'Vect2D':
        """Retourne un vecteur issu de la reprÃ©sentation polaire passÃ©e en
        argument.

        La reprÃ©sentation finale du vecteur est toujours selon un
        systÃ¨me de coordonnÃ©es cartÃ©siennes.

        L'orientation est en radians.

        Args:
            length (float): La longueur de la coordonnÃ©e polaire.
            orientation (float): L'orientation' de la coordonnÃ©e polaire.

        Exemples:
            >>> from math import pi
            >>> v1 = round(Vect2D.from_polar(5.0, pi/2.))
            >>> print(v1)
            (0.00E+00, 5.00E+00)
        """
        return cls(cos(orientation) * length, sin(orientation) * length)

    @classmethod
    def from_polar_degrees(cls, length: float, orientation: float) -> 'Vect2D':
        """Retourne un vecteur issu de la reprÃ©sentation polaire passÃ©e en
        argument.

        La reprÃ©sentation finale du vecteur est toujours selon un
        systÃ¨me de coordonnÃ©es cartÃ©siennes.

        L'orientation est en degrÃ©es.

        Args:
            length (float): La longueur de la coordonnÃ©e polaire.
            orientation (float): L'orientation' de la coordonnÃ©e polaire.

        Exemples:
            >>> v1 = round(Vect2D.from_polar_degrees(5.0, 90.))
            >>> print(v1)
            (0.00E+00, 5.00E+00)
        """
        return cls.from_polar(length, radians(orientation))

    def set_polar(self, length: float, orientation: float) -> None:
        """DÃ©termine le vecteur courant par la reprÃ©sentation polaire passÃ©e en
        argument.

        La reprÃ©sentation finale du vecteur est toujours selon un
        systÃ¨me de coordonnÃ©es cartÃ©siennes.

        L'orientation est en radians.

        Args:
            length (float): La longueur de la coordonnÃ©e polaire.
            orientation (float): L'orientation' de la coordonnÃ©e polaire.

        Exemples:
            >>> from math import pi
            >>> Vect2D.set_value_format(False, 1)
            >>> v1 = Vect2D()
            >>> v1.set_polar(5.0, pi/2.)
            >>> print(v1)
            (0.0, 5.0)
            >>> Vect2D.set_value_format(True, 2)
        """
        self.x = length * cos(orientation)
        self.y = length * sin(orientation)

    @property
    def length_squared(self) -> float:
        """`Read & Write`

        La longueur du vecteur au carrÃ©.

        Correspond Ã  la distance au carrÃ© du systÃ¨me de coordonnÃ©es polaires.
        La mÃ©trique retournÃ©e correspond Ã  la distance euclidienne.

        Exemples:
            >>> v1 = Vect2D(1.0, 2.0)
            >>> v1.length_squared
            5.0
        """
        return self.x ** 2. + self.y ** 2.

    @length_squared.setter
    def length_squared(self, value: float) -> None:
        self.set_polar(sqrt(value), self.orientation)

    @property
    def length(self) -> float:
        """`Read & Write`

        La longueur du vecteur.

        Correspond Ã  la distance du systÃ¨me de coordonnÃ©es polaires.
        La mÃ©trique retournÃ©e correspond Ã  la distance euclidienne.

        Exemples:
            >>> v1 = Vect2D(1.0, 1.0)
            >>> v1.length
            1.4142135623730951
        """
        return sqrt(self.length_squared)

    @length.setter
    def length(self, value: float) -> None:
        self.set_polar(value, self.orientation)

    @property
    def orientation(self) -> float:
        """`Read & Write`

        L'orientation du vecteur.

        Correspond Ã  l'orientation du systÃ¨me de coordonnÃ©es polaires.
        La mÃ©trique retournÃ©e est l'angle en radians.

        Exemples:
            >>> v1 = Vect2D(1.0, 1.0)
            >>> v1.orientation
            0.7853981633974483
        """
        return atan2(self.y, self.x)

    @orientation.setter
    def orientation(self, value: float) -> None:
        self.set_polar(self.length, value)

    @property
    def orientation_degrees(self) -> float:
        """`Read & Write`

        L'orientation du vecteur.

        Correspond Ã  l'orientation du systÃ¨me de coordonnÃ©es polaires.
        La mÃ©trique retournÃ©e est l'angle en degrÃ©es.

        Exemples:
            >>> v1 = Vect2D(1.0, 1.0)
            >>> v1.orientation_degrees
            45.0
        """
        return degrees(atan2(self.y, self.x))

    @orientation_degrees.setter
    def orientation_degrees(self, value: float) -> None:
        self.set_polar(self.length, radians(value))

    def limit_length_squared(self, max_length_squared: float) -> None:
        """Limite la longueur au carrÃ© du vecteur.

        Si la longueur au carrÃ© est plus petite que la limite, le vecteur
        reste inchangÃ©. Si la longueur au carrÃ© est plus grande, le vecteur
        est limitÃ© Ã  la longueur au carrÃ© maximum indiquÃ©e.

        Args:
            max_length_squared (float): La longueur au carrÃ© maximum que le
            vecteur peut avoir. Cette longueur doit Ãªtre strictement positive.
            (max_length_squared > 0.0)

        Exemples:
            >>> v1 = Vect2D(5.0, 0.0)
            >>> v1.limit_length_squared(9.0)
            >>> print(v1)
            (3.00E+00, 0.00E+00)
            >>> v1.limit_length_squared(25.0)
            >>> print(v1)
            (3.00E+00, 0.00E+00)
        """
        if self.length_squared > max_length_squared:
            self.length_squared = max_length_squared

    def limit_length(self, max_length: float) -> None:
        """Limite la longueur du vecteur.

        Si la longueur est plus petite que la limite, le vecteur reste
        inchangÃ©. Si la longueur est plus grande, le vecteur est limitÃ©
        Ã  la longueur maximum indiquÃ©e.

        Args:
            max_length (float): La longueur maximum que le vecteur peut
            avoir. Cette longueur doit Ãªtre strictement positive.
            (max_length_squared > 0.0)

        Exemples:
            >>> v1 = Vect2D(0.0, 5.0)
            >>> v1.limit_length(3.0)
            >>> print(round(v1))
            (0.00E+00, 3.00E+00)
            >>> v1.limit_length(5.0)
            >>> print(round(v1))
            (0.00E+00, 3.00E+00)
        """
        if self.length_squared > max_length * max_length:
            self.length = max_length

    def clamp_length_squared(self, min_length_squared: float, max_length_squared: float) -> None:
        """Borne la longueur au carrÃ© du vecteur.

        La longueur au carrÃ© est bornÃ©e aux limites infÃ©rieures et supÃ©rieures.

        0 < min_length_squared < max_length_squared

        Args:
            min_length_squared (float): La longueur au carrÃ© minimum que le
                vecteur peut avoir. Cette longueur doit Ãªtre strictement
                positive et infÃ©rieure Ã  la longueur au carrÃ© maximum.
            max_length_squared (float): La longueur au carrÃ© maximum que le
                vecteur peut avoir. Cette longueur doit Ãªtre strictement
                positive et supÃ©rieure Ã  la longueur au carrÃ© minimum.

        Exemples:
            >>> v1 = Vect2D(5.0, 0.0)
            >>> v1.clamp_length_squared(9.0, 16.0)
            >>> print(v1)
            (4.00E+00, 0.00E+00)
            >>> v1.clamp_length_squared(9.0, 25.0)
            >>> print(v1)
            (4.00E+00, 0.00E+00)
        """
        length_squared = self.length_squared
        if length_squared < min_length_squared:
            self.length_squared = min_length_squared
        elif length_squared > max_length_squared:
            self.length_squared = max_length_squared

    def clamp_length(self, min_length: float, max_length: float) -> None:
        """Borne la longueur du vecteur.

        La longueur est bornÃ©e aux limites infÃ©rieures et supÃ©rieures.

        0 < min_length < max_length

        Args:
            min_length (float): La longueur minimum que le vecteur peut
                avoir. Cette longueur doit Ãªtre strictement positive et
                infÃ©rieure Ã  la longueur maximum.
            max_length (float): La longueur maximum que le vecteur peut
                avoir. Cette longueur doit Ãªtre strictement positive et
                supÃ©rieure Ã  la longueur minimum.

        Exemples:
            >>> v1 = Vect2D(5.0, 0.0)
            >>> v1.clamp_length(3.0, 4.0)
            >>> print(v1)
            (4.00E+00, 0.00E+00)
            >>> v1.clamp_length(3.0, 5.0)
            >>> print(v1)
            (4.00E+00, 0.00E+00)
        """
        length_sqared = self.length_squared
        if length_sqared < min_length * min_length:
            self.length = min_length
        elif length_sqared > max_length * max_length:
            self.length = max_length

    # to do
    # def clamp_orientation(self, orientation_from : float, orientation_to : float) -> None:
    #     # orientation = self.orientation
    #     ...

    # --------------------------------------------------------------------
    #    _   _                            _ _          _   _
    #   | \ | | ___  _ __ _ __ ___   __ _| (_)______ _| |_(_) ___  _ __
    #   |  \| |/ _ \| '__| '_ ` _ \ / _` | | |_  / _` | __| |/ _ \| '_ \
    #   | |\  | (_) | |  | | | | | | (_| | | |/ / (_| | |_| | (_) | | | |
    #   |_| \_|\___/|_|  |_| |_| |_|\__,_|_|_/___\__,_|\__|_|\___/|_| |_|
    #
    # --------------------------------------------------------------------

    @property
    def is_normalized(self) -> bool:
        """`Read only`

        Est-ce que le vecteur est normalisÃ©.

        Un vecteur normalisÃ© est un vecteur unitaire (de longueur 1.0).

        Exemples:
            >>> v1 = Vect2D()
            >>> v2 = Vect2D(1.0, 0.0)
            >>> v1.is_normalized
            False
            >>> v2.is_normalized
            True
        """
        return isclose(self.length_squared, 1.0)

    @property
    def normalized(self) -> 'Vect2D':
        """`Read only`

        Retourne une nouvelle instance de 'Vect2D' correspondant au vecteur
        unitaire du vecteur courant.

        Le vecteur doit Ãªtre dÃ©fini.

        Exemples:
            >>> v1 = Vect2D(2.0, 0.0)
            >>> v2 = v1.normalized
            >>> print(v2)
            (1.00E+00, 0.00E+00)
        """
        vect = Vect2D(self.x, self.y)
        vect.normalize()
        return vect

    def normalize(self) -> None:
        """Modifie le vecteur courant pour qu'il soit unitaire.
        Cette transformation garde l'angle du vecteur.

        Le vecteur doit Ãªtre dÃ©fini.

        Exemples:
            >>> v1 = Vect2D(2.0, 0.0)
            >>> v1.normalize()
            >>> print(v1)
            (1.00E+00, 0.00E+00)
        """
        if self.is_defined:
            norm = self.length
            self.x /= norm
            self.y /= norm
        else:
            raise RuntimeError('cannot normalize a non defined vector')

    # ------------------------------------------------------------------------
    #    ____                 _                 _          _   _
    #   |  _ \ __ _ _ __   __| | ___  _ __ ___ (_)______ _| |_(_) ___  _ __
    #   | |_) / _` | '_ \ / _` |/ _ \| '_ ` _ \| |_  / _` | __| |/ _ \| '_ \
    #   |  _ < (_| | | | | (_| | (_) | | | | | | |/ / (_| | |_| | (_) | | | |
    #   |_| \_\__,_|_| |_|\__,_|\___/|_| |_| |_|_/___\__,_|\__|_|\___/|_| |_|
    #
    # ------------------------------------------------------------------------

    def randomize_normalized(self) -> None:
        """Modifie le vecteur courant de faÃ§on Ã  crÃ©er un vecteur unitaire alÃ©atoire.

        Exemples:
            >>> v1 = Vect2D()
            >>> v1.randomize_normalized()
            >>> print(v1) # doctest: +SKIP
            (1.00E+00, 0.00E+00)
        """
        self.set_polar(1.0, uniform(0., tau))

    def randomize_cartesian(self, x_min: float, x_max: float, y_min: float, y_max: float) -> None:
        """Modifie le vecteur courant de faÃ§on Ã  crÃ©er un vecteur alÃ©atoire
        paramÃ©trÃ© dans le systÃ¨me de coordonnÃ©es cartÃ©siennes.

        Args:
            x_min (float): La borne infÃ©rieure sur l'axe des abscisses.
            x_max (float): La borne supÃ©rieure sur l'axe des abscisses.
            y_min (float): La borne infÃ©rieure sur l'axe des ordonnÃ©es.
            y_max (float): La borne supÃ©rieure sur l'axe des ordonnÃ©es.

        Exemples:
            >>> v1 = Vect2D()
            >>> v1.randomize_cartesian(0., 100., 0, 100.)
            >>> print(v1) # doctest: +SKIP
            (12.00E+00, 77.00E+00)
        """
        self.x = uniform(x_min, x_max)
        self.y = uniform(y_min, y_max)

    # def randomize_polar(self, minLength, maxLength, minOrientation=0., maxOrientation=tau) -> None:
    #     self.set_polar(uniform(minLength, maxLength), uniform(minOrientation, maxOrientation))
    def randomize_polar(self, length_min: float, length_max: float, orientation_half_span: float = tau,
                        orientation_reference: float = 0.) -> None:
        """Modifie le vecteur courant de faÃ§on Ã  crÃ©er un vecteur alÃ©atoire
        paramÃ©trÃ© dans le systÃ¨me de coordonnÃ©es polaires.

        L'orientation est dÃ©finie en radians.

        Args:
            length_min (float): La longueur infÃ©rieure (sur l'axe des distances).
            length_max (float): La longueur spÃ©rieure (sur l'axe des distances).
            orientation_half_span (float): L'Ã©tendu de l'orientation en radians (sur l'axe de rotation). Defaults = tau
            orientation_reference (float): L'angle de rÃ©fÃ©rence en radians (sur l'axe de rotation). Defaults = 0.

        Exemples:
            >>> v1 = Vect2D()
            >>> v1.randomize_polar(0., 100., 0., 3.14)
            >>> print(v1) # doctest: +SKIP
            (12.00E+00, 28.00E+00)
        """
        self.set_polar(uniform(length_min, length_max),
                       uniform(-orientation_half_span, orientation_half_span) + orientation_reference)

    def randomize_polar_degrees(self, length_min: float, length_max: float, orientation_half_span: float = 360.,
                                orientation_reference: float = 0.) -> None:
        """Modifie le vecteur courant de faÃ§on Ã  crÃ©er un vecteur alÃ©atoire
        paramÃ©trÃ© dans le systÃ¨me de coordonnÃ©es polaires.

        L'orientation est dÃ©finie en degrÃ©es.

        Args:
            length_min (float): La longueur infÃ©rieure (sur l'axe des distances).
            length_max (float): La longueur spÃ©rieure (sur l'axe des distances).
            orientation_half_span (float): L'Ã©tendu de l'orientation en degrÃ©es (sur l'axe de rotation). Defaults = 360.
            orientation_reference (float): L'angle de rÃ©fÃ©rence en degrÃ©es (sur l'axe de rotation). Defaults = 0.

        Exemples:
            >>> v1 = Vect2D()
            >>> v1.randomize_polar(0., 100., 0., 90.)
            >>> print(v1) # doctest: +SKIP
            (12.00E+00, 28.00E+00)
        """
        self.randomize_polar(length_min, length_max, radians(orientation_half_span), radians(orientation_reference))

    @classmethod
    def from_random_normalized(cls) -> 'Vect2D':
        """CrÃ©e une nouvelle instance de 'Vect2D' correspondant Ã  vecteur unitaire alÃ©atoire.

        Exemples:
            >>> v1 = Vect2D.from_random_normalized()
            >>> print() # doctest: +SKIP
            (1.00E+00, 0.00E+00)
        """
        vect2d = cls()
        vect2d.randomize_normalized()
        return vect2d

    @classmethod
    def from_random_cartesian(cls, x_min: float, x_max: float, y_min: float, y_max: float) -> 'Vect2D':
        """CrÃ©e une nouvelle instance de 'Vect2D' alÃ©atoirement paramÃ©trÃ©
        dans le systÃ¨me de coordonnÃ©es cartÃ©siennes.

        Args:
            x_min (float): La borne infÃ©rieure sur l'axe des abscisses.
            x_max (float): La borne supÃ©rieure sur l'axe des abscisses.
            y_min (float): La borne infÃ©rieure sur l'axe des ordonnÃ©es.
            y_max (float): La borne supÃ©rieure sur l'axe des ordonnÃ©es.

        Exemples:
            >>> v1 = Vect2D.from_random_cartesian(0., 100., 0, 100.)
            >>> print(v1) # doctest: +SKIP
            (12.00E+00, 77.00E+00)
        """
        vect2d = cls()
        vect2d.randomize_cartesian(x_min, x_max, y_min, y_max)
        return vect2d

    @classmethod
    def from_random_polar(cls, length_min: float, length_max: float, orientation_half_span: float = tau,
                          orientation_reference: float = 0.) -> 'Vect2D':
        """CrÃ©e une nouvelle instance de 'Vect2D' alÃ©atoirement paramÃ©trÃ©
        dans le systÃ¨me de coordonnÃ©es polaires.

        L'orientation est dÃ©finie en radians.

        Args:
            length_min (float): La longueur infÃ©rieure (sur l'axe des distances).
            length_max (float): La longueur spÃ©rieure (sur l'axe des distances).
            orientation_half_span (float): L'Ã©tendu de l'orientation en radians (sur l'axe de rotation). Defaults = tau
            orientation_reference (float): L'angle de rÃ©fÃ©rence en radians (sur l'axe de rotation). Defaults = 0.

        Exemples:
            >>> v1 = Vect2D.from_random_polar(0., 100., 0., 3.14)
            >>> print(v1) # doctest: +SKIP
            (12.00E+00, 28.00E+00)
        """
        vect2d = cls()
        vect2d.randomize_polar(length_min, length_max, orientation_half_span, orientation_reference)
        return vect2d

    @classmethod
    def from_random_polar_degrees(cls, length_min: float, length_max: float, orientation_half_span: float = 360.,
                                  orientation_reference: float = 0.) -> 'Vect2D':
        """CrÃ©e une nouvelle instance de 'Vect2D' alÃ©atoirement paramÃ©trÃ©
        dans le systÃ¨me de coordonnÃ©es polaires.

        L'orientation est dÃ©finie en degrÃ©es.

        Args:
            length_min (float): La longueur infÃ©rieure (sur l'axe des distances).
            length_max (float): La longueur spÃ©rieure (sur l'axe des distances).
            orientation_half_span (float): L'Ã©tendu de l'orientation en degrÃ©es (sur l'axe de rotation). Defaults = 360.
            orientation_reference (float): L'angle de rÃ©fÃ©rence en degrÃ©es (sur l'axe de rotation). Defaults = 0.

        Exemples:
            >>> v1 = Vect2D()
            >>> v1.randomize_polar(0., 100., 0., 90.)
            >>> print(v1) # doctest: +SKIP
            (12.00E+00, 28.00E+00)
        """
        return cls.from_random_polar_degrees(length_min, length_max, radians(orientation_half_span),
                                             radians(orientation_reference))

    # ------------------------------------------------------------------------------------------------------------
    #   __        __         _    _                        _ _   _       ____   __     __        _   ____  ____
    #   \ \      / /__  _ __| | _(_)_ __   __ _  __      _(_) |_| |__   |___ \  \ \   / /__  ___| |_|___ \|  _ \
    #    \ \ /\ / / _ \| '__| |/ / | '_ \ / _` | \ \ /\ / / | __| '_ \    __) |  \ \ / / _ \/ __| __| __) | | | |
    #     \ V  V / (_) | |  |   <| | | | | (_| |  \ V  V /| | |_| | | |  / __/    \ V /  __/ (__| |_ / __/| |_| |
    #      \_/\_/ \___/|_|  |_|\_\_|_| |_|\__, |   \_/\_/ |_|\__|_| |_| |_____|    \_/ \___|\___|\__|_____|____/
    #                                     |___/
    # ------------------------------------------------------------------------------------------------------------

    def distance_squared_from(self, other: 'Vect2D') -> float:
        """Retourne la distance euclidienne au carrÃ© entre ce vecteur et
        celui passÃ© en argument.

        Args:
            other (Vect2D): L'autre vecteur dont la distance est Ã  Ã©valuer.

        Exemples:
            >>> v1 = Vect2D(8.0, -2.0)
            >>> v2 = Vect2D(12.0, -5.0)
            >>> v1.distance_squared_from(v2)
            25.0
        """
        return (self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y)

    def distance_from(self, other: 'Vect2D') -> float:
        """Retourne la distance euclidienne entre ce vecteur et celui
        passÃ© en argument.

        Args:
            other (Vect2D): L'autre vecteur dont la distance est Ã  Ã©valuer.

        Exemples:
            >>> v1 = Vect2D(8.0, -2.0)
            >>> v2 = Vect2D(12.0, -5.0)
            >>> v1.distance_from(v2)
            5.0
        """
        return sqrt(self.distance_squared_from(other))

    def is_perpendicular_to(self, other: 'Vect2D') -> bool:
        """Retourne 'True' si ce vecteur est perpendiculaire Ã  celui
        passÃ© en argument. Sinon retourne 'False'.

        Args:
            other (Vect2D): L'autre vecteur Ã  comparer.

        Exemples:
            >>> v1 = Vect2D(8.0, -2.0)
            >>> v2 = Vect2D(12.0, -5.0)
            >>> v1.is_perpendicular_to(v2)
            False
            >>> v1.is_perpendicular_to(v1.right_perpendicular)
            True
        """
        return isclose(self.dot(other), 0.0)

    def is_parallel_to(self, other: 'Vect2D') -> bool:
        """Retourne 'True' si ce vecteur est perpendiculaire Ã  celui
        passÃ© en argument. Sinon retourne 'False'.

        Args:
            other (Vect2D): L'autre vecteur Ã  comparer.

        Exemples:
            >>> v1 = Vect2D(8.0, -2.0)
            >>> v2 = Vect2D(12.0, -5.0)
            >>> v1.is_parallel_to(v2)
            False
            >>> v1.is_parallel_to(v1.right_perpendicular.right_perpendicular)
            True
        """
        return isclose(self.cross(other), 0.0)
        # return self.is_perpendicular_to(other.right_perpendicular)

    def is_forming_accute_angle_with(self,
                                     other: 'Vect2D') -> bool:  # the ~ same direction : acute angle 0 <= theta <= 90
        """Retourne 'True' si ce vecteur et celui passÃ© en argument forment
        un angle aigu. Sinon retourne 'False'.

        Args:
            other (Vect2D): L'autre vecteur Ã  comparer.

        Exemples:
            >>> v1 = Vect2D.from_polar_degrees(10.0, 45.0)
            >>> v2 = Vect2D.from_polar_degrees(10.0, 75.0)
            >>> v3 = Vect2D.from_polar_degrees(10.0, 185.0)
            >>> v1.is_forming_accute_angle_with(v2)
            True
            >>> v1.is_forming_accute_angle_with(v3)
            False
        """
        return self.dot(other) > 0.0

    def is_forming_obtuse_angle_with(self,
                                     other: 'Vect2D') -> bool:  # the ~ opposite direction : obtuse angle 90 <= theta <= 180
        return self.dot(other) < 0.0

    # -----------------------------------------
    #    ____                _            _
    #   |  _ \ _ __ ___   __| |_   _  ___| |_
    #   | |_) | '__/ _ \ / _` | | | |/ __| __|
    #   |  __/| | | (_) | (_| | |_| | (__| |_
    #   |_|   |_|  \___/ \__,_|\__,_|\___|\__|
    #
    # -----------------------------------------
    def dot(self, other: 'Vect2D') -> float:
        """Retourne le produit scalaire de ce vecteur avec celui passÃ© en
        argument.

        Args:
            other (Vect2D): L'autre vecteur.

        Exemples:
            >>> v1 = Vect2D(2.0, -5.0)
            >>> v2 = Vect2D(-3.0, 2.0)
            >>> v1.dot(v2)
            -16.0
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other: 'Vect2D') -> float:
        """Retourne le produit vectoriel de ce vecteur avec celui passÃ© en
        argument.

        Args:
            other (Vect2D): L'autre vecteur.

        Exemples:
            >>> v1 = Vect2D(2.0, -5.0)
            >>> v2 = Vect2D(-3.0, 2.0)
            >>> v1.cross(v2)
            -11.0
        """
        return self.x * other.y - self.y * other.x

    # def translate(self, ...)
    # def rotate(self, ...)
    # def scale(self, ...)
    # def transform(self, ...)

    # ----------------------------------------------------------------------------------------------------
    #    ____            _           _   _                  __  ____       _           _   _
    #   |  _ \ _ __ ___ (_) ___  ___| |_(_) ___  _ __      / / |  _ \ ___ (_) ___  ___| |_(_) ___  _ __
    #   | |_) | '__/ _ \| |/ _ \/ __| __| |/ _ \| '_ \    / /  | |_) / _ \| |/ _ \/ __| __| |/ _ \| '_ \
    #   |  __/| | | (_) | |  __/ (__| |_| | (_) | | | |  / /   |  _ <  __/| |  __/ (__| |_| | (_) | | | |
    #   |_|   |_|  \___// |\___|\___|\__|_|\___/|_| |_| /_/    |_| \_\___|/ |\___|\___|\__|_|\___/|_| |_|
    #                 |__/                                              |__/
    # ----------------------------------------------------------------------------------------------------
    def angle_between(self, other: 'Vect2D') -> float:  # in radians
        """Retourne l'angle crÃ©Ã© avec le vecteur passÃ© en argument.

        L'angle est en radians.

        Args:
            other (Vect2D): L'autre vecteur formant l'angle.

        Exemples:
            >>> from math import isclose, pi, degrees
            >>> v1 = Vect2D(5.0, 5.0)
            >>> v2 = Vect2D.from_polar_degrees(5.0, 67.5)
            >>> isclose(v1.angle_between(v2), pi / 8.0)
            True
            >>> round(degrees(v1.angle_between(v2)), 1)
            22.5
        """
        return acos(self.dot(other) / sqrt(self.length_squared * other.length_squared))

    def angle_between_degrees(self, other: 'Vect2D') -> float:
        """Retourne l'angle crÃ©Ã© avec le vecteur passÃ© en argument.

        L'angle est en degrÃ©es.

        Args:
            other (Vect2D): L'autre vecteur formant l'angle.

        Exemples:
            >>> from math import isclose, pi, degrees
            >>> v1 = Vect2D(5.0, 5.0)
            >>> v2 = Vect2D.from_polar_degrees(5.0, 67.5)
            >>> isclose(v1.angle_between_degrees(v2), 22.5)
            True
            >>> round(v1.angle_between_degrees(v2),1)
            22.5
        """
        return degrees(self.angle_between(other))

    def angle_disparity(self, other: 'Vect2D') -> float:  # angle in radians with direction
        """Retourne l'angle crÃ©Ã© avec le vecteur passÃ© en argument.
        La direction de l'angle est donnÃ© contrairement Ã  la fonction
        angle_between :
         - si l'angle est nÃ©gatif, l'autre vecteur se trouve dans le sens
           inverse de rotation
         - si l'angle est positif, l'autre vecteur se trouve dans le sens
           de rotation

        L'angle est en radians.

        Args:
            other (Vect2D): L'autre vecteur formant l'angle.

        Exemples:
            >>> from math import isclose, pi, degrees
            >>> v1 = Vect2D(5.0, 5.0)
            >>> v2 = Vect2D.from_polar_degrees(5.0, 67.5)
            >>> isclose(v1.angle_disparity(v2), pi / 8.0)
            True
            >>> round(degrees(v1.angle_disparity(v2)), 1)
            22.5
            >>> round(degrees(v2.angle_disparity(v1)), 1)
            -22.5
        """
        return atan2(self.cross(other), self.x * other.x + self.y * other.y)

    def angle_disparity_degrees(self, other: 'Vect2D') -> float:  # angle in radians with direction
        """Retourne l'angle crÃ©Ã© avec le vecteur passÃ© en argument.
        La direction de l'angle est donnÃ© contrairement Ã  la fonction
        angle_between :
         - si l'angle est nÃ©gatif, l'autre vecteur se trouve dans le sens
           inverse de la rotation
         - si l'angle est positif, l'autre vecteur se trouve dans le sens
           de la rotation

        L'angle est en degrÃ©es.

        Args:
            other (Vect2D): L'autre vecteur formant l'angle.

        Exemples:
            >>> from math import isclose
            >>> v1 = Vect2D(5.0, 5.0)
            >>> v2 = Vect2D.from_polar_degrees(5.0, 67.5)
            >>> isclose(v1.angle_disparity_degrees(v2), 22.5)
            True
            >>> round(v1.angle_disparity_degrees(v2), 1)
            22.5
            >>> round(v2.angle_disparity_degrees(v1), 1)
            -22.5
        """
        return degrees(self.angle_disparity(other))

    def scalar_projection(self, other: 'Vect2D') -> float:
        """Retourne la projection scalaire de ce vecteur sur le vecteur passÃ©
        en argument.

        Args:
            other (Vect2D): Le vecteur sur lequel est projetÃ© le vecteur
            courant.

        Exemples:
            >>> v1 = Vect2D(3.0, 1.0)
            >>> v2 = Vect2D(5.0, 0.0)
            >>> v1.scalar_projection(v2)
            3.0
        """
        return self.dot(other) / other.length

    def vector_projection(self, other: 'Vect2D') -> 'Vect2D':
        """Retourne la projection vectorielle de ce vecteur sur le vecteur passÃ©
        en argument.

        Args:
            other (Vect2D): Le vecteur sur lequel est projetÃ© le vecteur
            courant.

        Exemples:
            >>> v1 = Vect2D(3.0, 1.0)
            >>> v2 = Vect2D(5.0, 0.0)
            >>> print(v1.vector_projection(v2))
            (3.00E+00, 0.00E+00)
        """
        return self.dot(other) / other.dot(other) * other

    def scalar_rejection(self, other: 'Vect2D') -> float:
        """Retourne la rÃ©jection scalaire de ce vecteur sur le vecteur passÃ©
        en argument.

        Args:
            other (Vect2D): Le vecteur sur lequel est projetÃ© le vecteur
            courant.

        Exemples:
            >>> v1 = Vect2D(3.0, 1.0)
            >>> v2 = Vect2D(5.0, 0.0)
            >>> v1.scalar_rejection(v2)
            1.0
        """
        return (self.y * other.x - self.x * other.y) / other.length

    def vector_rejection(self, other: 'Vect2D') -> 'Vect2D':
        """Retourne la rÃ©jection vectorielle de ce vecteur sur le vecteur passÃ©
        en argument.

        Args:
            other (Vect2D): Le vecteur sur lequel est projetÃ© le vecteur
            courant.

        Exemples:
            >>> v1 = Vect2D(3.0, 1.0)
            >>> v2 = Vect2D(5.0, 0.0)
            >>> print(v1.vector_rejection(v2))
            (0.00E+00, 1.00E+00)
        """
        return self - self.vector_projection(other)

    def projection_analysis(self, other: 'Vect2D') -> tuple[float, 'Vect2D', float, 'Vect2D']:
        """Retourne l'analyse complÃ¨te de la projection de ce vecteur sur le vecteur passÃ©
        en argument.

        Args:
            other (Vect2D): Le vecteur sur lequel est projetÃ© le vecteur
            courant.

        Returns:
            un tuple contenant :
             - la projection scalaire
             - la projection vectorielle
             - la rÃ©jection scalaire
             - la rÃ©jection vectorielle

        Exemples:
            >>> v1 = Vect2D(3.0, 1.0)
            >>> v2 = Vect2D(5.0, 0.0)
            >>> analysis = v1.projection_analysis(v2)
            >>> print(f'Projection : {analysis[0]} | {analysis[1]}')
            Projection : 3.0 | (3.00E+00, 0.00E+00)
            >>> print(f'RÃ©jection : {analysis[2]} | {analysis[3]}')
            RÃ©jection : 1.0 | (0.00E+00, 1.00E+00)
        """
        scalar_proj = self.scalar_projection(other)
        vector_proj = scalar_proj * other.normalized
        scalar_rej = self.scalar_rejection(other)
        vector_rej = self - vector_proj

        return (scalar_proj, vector_proj, scalar_rej, vector_rej)

    # ---------------------------------------------------------------------------------------------------------
    #     ___                       _                                       _                 _ _
    #    / _ \ _ __   ___ _ __ __ _| |_ ___  _ __ ___    _____   _____ _ __| | ___   __ _  __| (_)_ __   __ _
    #   | | | | '_ \ / _ \ '__/ _` | __/ _ \| '__/ __|  / _ \ \ / / _ \ '__| |/ _ \ / _` |/ _` | | '_ \ / _` |
    #   | |_| | |_) |  __/ | | (_| | || (_) | |  \__ \ | (_) \ V /  __/ |  | | (_) | (_| | (_| | | | | | (_| |
    #    \___/| .__/ \___|_|  \__,_|\__\___/|_|  |___/  \___/ \_/ \___|_|  |_|\___/ \__,_|\__,_|_|_| |_|\__, |
    #         |_|                                                                                       |___/
    # ---------------------------------------------------------------------------------------------------------

    def __eq__(self, other: 'Vect2D') -> bool:  # self == other
        """
        >>> v1 = Vect2D()
        >>> v2 = Vect2D(1.0, -1.5)
        >>> v3 = Vect2D(1.0, -1.5)
        >>> v1 == v2
        False
        >>> v2 == v3
        True
        """
        return isclose(self.x, other.x) and isclose(self.y, other.y)

    def __ne__(self, other: 'Vect2D') -> bool:  # self != other
        """
        >>> v1 = Vect2D()
        >>> v2 = Vect2D(1.0, -1.5)
        >>> v3 = Vect2D(1.0, -1.5)
        >>> v1 != v2
        True
        >>> v2 != v3
        False
        """
        return not (isclose(self.x, other.x) and isclose(self.y, other.y))

    def __neg__(self) -> 'Vect2D':  # -self
        """
        >>> v1 = Vect2D(1.0, -1.5)
        >>> print(-v1)
        (-1.00E+00, 1.50E+00)
        """
        return Vect2D(-self.x, -self.y)

    def __add__(self, other: 'Vect2D') -> 'Vect2D':  # self + other
        """
        >>> v1 = Vect2D(1.0, -1.5)
        >>> v2 = Vect2D(-2.0, 1.0)
        >>> print(v1 + v2)
        (-1.00E+00, -5.00E-01)
        """
        return Vect2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: 'Vect2D') -> 'Vect2D':  # self += other
        """
        >>> v1 = Vect2D(1.0, -1.5)
        >>> v1 += Vect2D(-2.0, 1.0)
        >>> print(v1)
        (-1.00E+00, -5.00E-01)
        """
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: 'Vect2D') -> 'Vect2D':  # self - other
        """
        >>> v1 = Vect2D(1.0, -1.5)
        >>> v2 = Vect2D(-2.0, 1.0)
        >>> print(v1 - v2)
        (3.00E+00, -2.50E+00)
        """
        return Vect2D(self.x - other.x, self.y - other.y)

    def __isub__(self, other: 'Vect2D') -> 'Vect2D':  # self -= other
        """
        >>> v1 = Vect2D(1.0, -1.5)
        >>> v1 -= Vect2D(-2.0, 1.0)
        >>> print(v1)
        (3.00E+00, -2.50E+00)
        """
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: float) -> 'Vect2D':  # self * other
        """
        >>> v1 = Vect2D(1.0, -1.5)
        >>> print(v1 * 5.0)
        (5.00E+00, -7.50E+00)
        """
        return Vect2D(self.x * other, self.y * other)

    def __rmul__(self, other: float) -> 'Vect2D':  # other * self
        """
        >>> v1 = Vect2D(1.0, -1.5)
        >>> print(5.0 * v1)
        (5.00E+00, -7.50E+00)
        """
        return Vect2D(self.x * other, self.y * other)

    def __imul__(self, other: float) -> 'Vect2D':  # self *= other
        """
        >>> v1 = Vect2D(1.0, -1.5)
        >>> v1 *= 5.0
        >>> print(v1)
        (5.00E+00, -7.50E+00)
        """
        self.x *= other
        self.y *= other
        return self

    def __truediv__(self, other: float) -> 'Vect2D':  # self / other
        """
        >>> v1 = Vect2D(1.0, -1.5)
        >>> print(v1 / 2.0)
        (5.00E-01, -7.50E-01)
        """
        return Vect2D(self.x / other, self.y / other)

    def __rtruediv__(self, other: float) -> 'Vect2D':  # other / self
        """
        >>> v1 = Vect2D(1.0, -1.5)
        >>> print(2.0 / v1)
        (2.00E+00, -1.33E+00)
        """
        return Vect2D(other / self.x, other / self.y)

    def __itruediv__(self, other: float) -> 'Vect2D':  # self /= other
        """
        >>> v1 = Vect2D(1.0, -1.5)
        >>> v1 /= 2.0
        >>> print(v1)
        (5.00E-01, -7.50E-01)
        """
        self.x /= other
        self.y /= other
        return self

    # --------------------------------------------------------------------------------------------------------
    #    _____                 _   _                                       _                 _ _
    #   |  ___|   _ _ __   ___| |_(_) ___  _ __  ___    _____   _____ _ __| | ___   __ _  __| (_)_ __   __ _
    #   | |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __|  / _ \ \ / / _ \ '__| |/ _ \ / _` |/ _` | | '_ \ / _` |
    #   |  _|| |_| | | | | (__| |_| | (_) | | | \__ \ | (_) \ V /  __/ |  | | (_) | (_| | (_| | | | | | (_| |
    #   |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/  \___/ \_/ \___|_|  |_|\___/ \__,_|\__,_|_|_| |_|\__, |
    #                                                                                                  |___/
    # --------------------------------------------------------------------------------------------------------

    def __abs__(self) -> 'Vect2D':  # abs(self)
        """Retourne les valeurs absolues de `x` et `y`.

        Retourne une nouvelle instance de `Vect2D` tout en ne modifiant pas
        l'instance courante. Les valeur `x` et `y` restent des `float` mÃªme
        si elles sont arrondies.

        Exemples:
            >>> v1 = Vect2D(2.25, -1.75)
            >>> v2 = abs(v1)
            >>> print(v2)
            (2.25E+00, 1.75E+00)
        """
        return Vect2D(abs(self.x), abs(self.y))

    def __round__(self, ndigits=None) -> 'Vect2D':  # round(self)
        """Arrondi les composantes x et y du vecteur vers l'entier le plus prÃ¨s.

        Retourne une nouvelle instance de `Vect2D` tout en ne modifiant pas
        l'instance courante. Les valeur `x` et `y` restent des `float` mÃªme
        si elles sont arrondies.

        Exemples:
            >>> v1 = Vect2D(2.25, -1.75)
            >>> v2 = round(v1)
            >>> print(v2)
            (2.00E+00, -2.00E+00)
        """
        return Vect2D(round(self.x, ndigits), round(self.y, ndigits))

    def __trunc__(self) -> 'Vect2D':  # trunc(self)
        """Arrondi les composantes x et y du vecteur vers zÃ©ro.

        Retourne une nouvelle instance de `Vect2D` tout en ne modifiant pas
        l'instance courante. Les valeur `x` et `y` restent des `float` mÃªme
        si elles sont arrondies.

        Exemples:
            >>> v1 = Vect2D(2.25, -1.75)
            >>> v2 = trunc(v1)
            >>> print(v2)
            (2.00E+00, -1.00E+00)
        """
        return Vect2D(trunc(self.x), trunc(self.y))

    def __floor__(self) -> 'Vect2D':  # floor(self)
        """Arrondi les composantes x et y du vecteur vers l'infini nÃ©gatif.

        Retourne une nouvelle instance de `Vect2D` tout en ne modifiant pas
        l'instance courante. Les valeur `x` et `y` restent des `float` mÃªme
        si elles sont arrondies.

        Exemples:
            >>> v1 = Vect2D(2.25, -1.75)
            >>> v2 = floor(v1)
            >>> print(v2)
            (2.00E+00, -2.00E+00)
        """
        return Vect2D(floor(self.x), floor(self.y))

    def __ceil__(self) -> 'Vect2D':  # ceil(self)
        """Arrondi les composantes x et y du vecteur vers l'infini positif.

        Retourne une nouvelle instance de `Vect2D` tout en ne modifiant pas
        l'instance courante. Les valeur `x` et `y` restent des `float` mÃªme
        si elles sont arrondies.

        Exemples:
            >>> v1 = Vect2D(2.25, -1.75)
            >>> v2 = ceil(v1)
            >>> print(v2)
            (3.00E+00, -1.00E+00)
        """
        return Vect2D(ceil(self.x), ceil(self.y))

    def __complex__(self) -> 'Vect2D':  # complex(self)
        """CrÃ©e un nombre complexe reprÃ©sentant le vecteur.

        Ne modifie pas l'instance courante.

        Exemples:
            >>> v1 = Vect2D(2.5, -1.5)
            >>> comp = complex(v1)
            >>> print(comp)
            (2.5-1.5j)
        """
        return complex(self.x, self.y)

    @classmethod
    def from_data(cls, data: tuple[float, float] | list[float, float] | dict[str, float]) -> 'Vect2D':
        """CrÃ©e une nouvelle instance de `Vect2D` Ã  partir d'une structure existante :
        - tuple ou liste de 2 float :
            - seulement 2 donnÃ©es
            - reprÃ©sentant le x et le y
            - (0.0, 0.0)
            - [0.0, 0.0]
        - dict de 2 float :
            - les clÃ©s doivent des str 'x' ou 'y'
            - toutes minuscules ou majuscules
            - { 'x':0.0, 'y':0.0 }
            - { 'X':0.0, 'Y':0.0 }

        Exemples:
            >>> v1 = Vect2D.from_data((1.0, 2.5))
            >>> print(v1)
            (1.00E+00, 2.50E+00)
            >>> v2 = Vect2D.from_data([1.0, 2.5])
            >>> print(v2)
            (1.00E+00, 2.50E+00)
            >>> v3 = Vect2D.from_data({'x':1.0, 'y':2.5})
            >>> print(v3)
            (1.00E+00, 2.50E+00)
            >>> v4 = Vect2D.from_data({'X':1.0, 'Y':2.5})
            >>> print(v4)
            (1.00E+00, 2.50E+00)
        """
        if isinstance(data, tuple) and len(data) == 2:
            return Vect2D(data[0], data[1])
        if isinstance(data, list) and len(data) == 2:
            return Vect2D(data[0], data[1])
        if isinstance(data, dict):
            k = set(data.keys())
            if k == {'x', 'y'}:
                return Vect2D(data['x'], data['y'])
            elif k == {'X', 'Y'}:
                return Vect2D(data['X'], data['Y'])
        else:
            raise TypeError("data is not compatible - must be a tuple/list of 2 float or a dict with 'x' or 'y'")

    @property
    def as_tuple(self) -> tuple[float, float]:
        """CrÃ©e et retourne un tuple de deux rÃ©els. La liste crÃ©Ã©e possÃ¨de
        les abscisses et les ordonnÃ©es dans l'ordre.

        Ne modifie pas l'instance courante.

        Exemples:
            >>> v1 = Vect2D(2.5, -1.5)
            >>> print(v1.as_tuple)
            (2.5, -1.5)
        """
        return (self.x, self.y)

    @property
    def as_list(self) -> list[float, float]:
        """CrÃ©e et retourne une liste de deux rÃ©els. La liste crÃ©Ã©e possÃ¨de
        les abscisses et les ordonnÃ©es dans l'ordre.

        Ne modifie pas l'instance courante.

        Exemples:
            >>> v1 = Vect2D(2.5, -1.5)
            >>> print(v1.as_list)
            [2.5, -1.5]
        """
        return [self.x, self.y]

    @property
    def as_dict(self) -> dict[str, int]:
        """CrÃ©e et retourne un dictionnaire de deux rÃ©els. Le dictionnaire
        possÃ¨de les clÃ©s suivantes :
        - 'x' : les abscisses
        - 'y' : les ordonnÃ©es

        Ne modifie pas l'instance courante.

        Exemples:
            >>> v1 = Vect2D(2.5, -1.5)
            >>> print(v1.as_dict)
            {'x': 2.5, 'y': -1.5}
        """
        return {'x': self.x, 'y': self.y}


Vect2D.UNDEFINED = Vect2D()
"""ReprÃ©sente un vecteur indÃ©fini. C'est Ã  dire le vecteur (0.0, 0.0)."""


def __main_doctest():
    if bool(__debug__):  # do not work
        import test
        doctest.testmod()  # verbose=True)


def __main_doctest():
    import test
    doctest.testmod()  # verbose=True)


if __name__ == "__main__":
    __main_doctest()