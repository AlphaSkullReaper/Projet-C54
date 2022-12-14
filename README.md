%# Projet-C54


<div align="center">
  <h3 align="center">Objets Connectés - Le Bon Vieux GoPiGo</h3>
</div>

## Les Membres <br>
Mathieu Beaupré <br>
Jonathan Frédéric <br>
Korallia Frenette <br>
William Lemire <br>

    
## La librairie FiniteStateMachine
98% de similitude avec le projet donné. Nous avons travaillé de manière ardue afin de respecter la conception le plus près possible. Nous ne nous avons pas laissé de liberté d'interprétation quant à la conception, nous voulions le suivre à la lettre.

Nous n'avons pas fait la surcharge des méthodes "turn_on/off" ni des "blink". Nous avons juste donné un nom unique à chaque fonction question d'avancer plus rapidement. 

Nous n'avons pas implémenté les méthodes "wink". 

Nous avons rajouté des méthodes statiques de création de transitions pour chaque type de transition dans le document de conception. Ceci rend la lecture des layouts plus facile. 

## L'infrastructure

### Classe Robot
Notre classe Robot sert à faire une abstraction sur le robot GoPiGo3 et de permettre l'utilisation des composantes électroniques. Donc, nous implémentons les fonctions déjà présentes dans la librairie GoPiGo, ainsi que d'autres méthodes de notre cru.

#### Validation de l'intégrité du robot
Puisque nous avons implémenté toutes les fonctions de la librairie GoPiGo dans notre classe Robot (duck typing), il a été simple d'appeler les méthodes d'initialisation des composantes électroniques dont nous avons besoin pour le projet. Donc, dans notre fonction d'entrée de l'état Integrity de la FiniteStateMachineC64, on appelle la création de la télécommande, de la LED, du télémètre et du servo-moteur. Si un seul échoue, nous allons vers l'état Integrity_Failed. 

#### Gestion de la télécommande
En premier lieu, nous avons une classe nommée RemoteControlTransition. Même si la seule différence entre cette transition et une ConditionalTransition est le type de condition pris (une RemoteControlTransition prend un objet RemoteControl), la classe RemoteControlTransition encapsule l'idée d'une transition faite avec la télécommande, permettant plus d'aise lors du débuggage puisqu'en un regard, nous savons que c'est une transition basée sur la télécommande.

Ensuite, nous avons créé une condition nommée RemoteValueCondition qui hérite de la classe Condition. Celle-ci a deux objectifs:
1) Faire la lecture de la télécommande
2) S'assurer qu'il n'y a qu'une lecture de valeur faite (empêcher que pour une touche pesée, nous recevions plusieurs valuers).


#### Gestion du télémètre et de son servo moteur
TOUT DOUX

#### Gestion de la couleur pour les yeux (EyeBlinkers)
Étant donné que nous avions déjà une classe robot qui représentait toutes les composantes électroniques et qui contenait déjà les fonctions de base de changement de couleur de la librairie GoPiGo, nous avons créé la notre qui prend un côté en argument ainsi qu'un tuple de couleur (0 à 255). Ensuite, elle assigne la couleur avec les méthodes préexistente de GopiGo, set_color(), et ensuite nous ouvrons les yeux pour appliquer le changement de couleur.

### Structure générale du projet
#### Infrastructure générale du logiciel
Classe C64:
Classe Robot:
Classe FiniteStateMachine:

#### Capacité module d'insertion d'une nouvelle tâche

