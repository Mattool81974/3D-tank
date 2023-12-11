# 3D-tank
> ## Presentation
>> ### What ?
>> 3D tank is a projet of creating a 3D simple tank game with python, made by a year 13/12th grade student.
>
>> ### Why ?
>> In France, the IT program in my class is very simple for a guys who's know how to code.
>> Creating a game like that is a bigger and most interesting project.
>> To see what kind's of projects we do, go watch my Github repositories.
>
>> ### How ?
>> As my first big project like that, the game will use Python.
>> Not because it's simple, but because we use to do it in classe.
>> The game will use a Doom-like engine.
>
>> ### Who ?
>> This project is made by a year 13/12th grade student behind the Mattool81974 nickname.
>> I started programming when I was 9 in C++, with the QT library.
>> When I joined IT class in my school, the French school program wants us to use mainly Python.
>> I'm the kind of guys who add a few useless and more advanced things into his school project for fun.
>> I'm also a big fans of military vehicules, and particulary from tanks.
>> But, I'm not used to do projects like that, it's my first time. Please be indulgent.
>> If you want to send me advices, contact me with this mail adress : matt.thunder.off@gmail.com
>> PS : Thunder is not my firstname.

> ## The Game
>> ### Gameplay
>> The gameplay will be very easy. It consist to a player controlling a tank turret (vertical and horizontal rotation of the cannon).
>> Some enemy tank will pass in the map, and the player will have to shot them. The player's tank is a French Leclerc, which can shot a nerfed OFL 120 F1.
>> The enemy tank can be Leopard 2A7, M1A2 Abrams or T-90 for the tanks, or Puma, M3A3 Bradley or BMP Terminator for light vehicules. They can't shot back at the user.
>> The damage engine is quite similar to the War Thunder damage engine, for exemple, an ammo in the engine will paralyze the tank.
>> The obstacle are permanently on the map (tree, rock...) and stop ammo. Some can be destroyed.
>> The player can see the map with a normal view (like on War Thunder) or a shooter view (yet like on War Thunder). The shooter view has a thermal view.
>> ### Graphic and physic
>> The game use a 3D engine inspired from Doom. The map is a 2D map, but the engine show it in 3D.
>> One part of the 2D map is a 1 meter square on the 3D engine. The physics engine use the 2D map to simulate collisions.
>> Every texture have a number assigned. Here a little list of texture and his number :
>> - 1 : nothing (floor, mainly grass).
>> - 2 : tree (inspired from Minecraft).
>> - 3 : rock (inspired from Minecraft).
>> - 4 : brick wall (inspired from Minecraft), may have a ceil.
>> - 5 : stone wall, may have a ceil.
>> - 6 : wood wall, may have a ceil.
>> - 7 : little hill.
>> - 8 : Leopard 2.
>> - 9 : M1A2 Abrams.
>> - 10 : T-90.
>> - 11 : Puma.
>> - 12 : M3A3 Bradley.
>> - 13 : BMP Terminator.
>> - 14 : Leclerc ceil.
>> The texture with the thermal view of each part is the opposite of the normal view texture number (it's what it don't start at 0).
>> ### Map
>> The main map is a 505 * 505 map which represents a plain, with the middle in 253 - 253, where the player tank is located (we will assume the player tank turret is 5 meter * 5 meter).
>> Each part has an id describing what is on this part. Here the ids possible for the part :
>> - 0 to 6 : same as texture id.
>> - 7 : player tank location.
>> The map will be stored into a binary file with the .agmff format (random letter, meaning "a good map file format").
>> The 4 first bytes describes the width and the height of the map with unsigned integer (in part).
>> The others width * eight 3 bytes describe for the 2 first bytes the number in unsigned integer of a part and the other bytes in signed integer the id of the part.

> ## Ressources
>> ### Sources
>> Here is some sources who help me to do this project.
>> https://www.youtube.com/watch?v=ECqUrT7IdqQ
