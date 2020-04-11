# Kumamon Run Run Run
* My game
* How to play
* Description of my code

## Game Introduction: 
Play as Kumamon, the cutest bear intent on stealing the most delicious honey in the world. Unfortunately, all honey are protected by security guards in a house. The only way to get them is secretly entering the house. Sneak past the security guards on your way to steal all honey. Use your wisdom and braveness to avoid detection and fulfil the greatest goal. Go play now!!! Good Luck!


## Rules :
**Kumamon Run Run Run** is a game that the player controls the motions and actions of a kumamon bear on the screen window using `w` `s` `a` `d` on the keyboard. Player can also speed up the movement of Kumamon by press down the `r` key. Player has **3** chances to speed up. The Main Goal of this game for player is to assist the Kumamon bear to steal all the honey (**6** in total) and at the same time avoid being caught be the guard men (**3** in total). After stealing all the honey, the player need to control the Kumamon bear to move out the house and return to initial position. The guard men will initially move in their scheduled routes. Hence a better way to play is observing the routes of them before taking actions. If the Kumamon bear is being seen or found by the guard men, they will run to catch the bear.(! They run very **FAST**). The player can know if Kumamon bear is being found by seeing the third label on the right side. The label is initially in green `Safe` and keep the same if no one found you. However, the label will turn Red 'Warn' if the guard men are trying to catch the bear. Each honey worths **1** point, player can see how many points obtained on the `Money` label right side. Player can also see how many chances left for Kumamon bear to speed up at `Speed up chance` label. The cd player can faciliate Kumamon when stealing honey. When player sets cd player to play cd, the security guards nearby will come to check what happen in 5 seconds. Player can use this time interval to steal honey. Notice it can only used once then it will disappear. 

## Code Description:
### Library / Module used:

Name | Function 
------|---------
 time | stop the game when require user to make decision
 kivy | build the kivy GUI for game
 numpy | help function when build the guards' routes
 libdw | construct the state machine for security guards
 
 
###  GUI:
> MyGame class 

#### Kumamon 
* Object : Rectangle class 
* Motion : keyboard function + bind method
* Steal Honey : catch function and change in money label value 
* Speed up : change in self.speed and speed label change 

#### Security Guard 
* Object : Rectangle class 
* Schedule : Clock.schedule_interval function  + self defined route boundary
* State Machine : Police class

#### Honey 
* Object : Rectangle class
* Event : if Kumamon catch it, it disappear and money label change

#### CD Player 
* Object : Rectangle class
* Play : if set to play, guard nearby will come to check 
#### House 
* Structure : Rectangle class + canvas widget

#### Labels
* Object : Rectangle class 
* Event : Change label texture 


### State Machine:
> Police class

####States: 

*  **Route** : At this state, guard will follow the scheduled route 
*  **Catch** : At this state, guard will move towards Kumamon 
*  **End** : At this state, guard aleady catch Kumamon, Game Ends

#### Inputs:
input data typy : **tuple type**

* **police** : Object, Contain all information of this guard
* **player** : Object, Contain all information of Kumamon
* **direction** : Int, The dirction of guard movement 

#### Transition :
Current State | Requirement | Next State
------|------|---
Route| Not detect Kumamon | Route
Route| Detect Kumamon| Catch
Catch | Kumamon in warning region | Catch
Catch | Kumamon out warning region | Route
Catch | Kumamon is caught by guard | End
End | Anything | End

### Others :
* catch function: check if two object collide with each others
* detect function: check if one object overlap with given boundary